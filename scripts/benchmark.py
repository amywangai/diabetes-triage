"""
Benchmark script to compare model versions.
"""
import time
import pickle
import json
import numpy as np
from pathlib import Path
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

RANDOM_SEED = 42


def load_model(model_path):
    """Load a trained model."""
    with open(model_path, 'rb') as f:
        return pickle.load(f)


def benchmark_model(model_path, X_test, y_test):
    """Benchmark a model's performance and speed."""
    print(f"\nBenchmarking {model_path.name}...")
    
    # Load model
    pipeline = load_model(model_path)
    
    # Measure prediction time
    start_time = time.time()
    X_scaled = pipeline["scaler"].transform(X_test)
    predictions = pipeline["model"].predict(X_scaled)
    end_time = time.time()
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    # Calculate speed metrics
    total_time = end_time - start_time
    time_per_sample = (total_time / len(X_test)) * 1000  # ms
    
    # Get model size
    model_size_mb = model_path.stat().st_size / (1024 * 1024)
    
    results = {
        "model": model_path.stem,
        "rmse": round(rmse, 2),
        "mae": round(mae, 2),
        "r2": round(r2, 4),
        "total_time_ms": round(total_time * 1000, 2),
        "time_per_sample_ms": round(time_per_sample, 4),
        "throughput_samples_per_sec": round(len(X_test) / total_time, 2),
        "model_size_mb": round(model_size_mb, 3)
    }
    
    return results


def main():
    """Run benchmark comparison."""
    print("🔬 Model Benchmark Comparison")
    print("=" * 60)
    
    # Load data
    diabetes = load_diabetes(as_frame=True)
    X = diabetes.frame.drop(columns=["target"])
    y = diabetes.frame["target"]
    
    # Split data (same as training)
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED
    )
    
    print(f"Test set size: {len(X_test)} samples")
    
    # Find all model files
    model_dir = Path("models")
    model_files = list(model_dir.glob("model*.pkl"))
    
    if not model_files:
        print("❌ No model files found. Please train a model first.")
        return
    
    # Benchmark each model
    results = []
    for model_path in model_files:
        result = benchmark_model(model_path, X_test, y_test)
        results.append(result)
    
    # Display results
    print("\n" + "=" * 60)
    print("📊 BENCHMARK RESULTS")
    print("=" * 60)
    
    for result in results:
        print(f"\n{result['model']}:")
        print(f"  Accuracy Metrics:")
        print(f"    RMSE: {result['rmse']}")
        print(f"    MAE:  {result['mae']}")
        print(f"    R²:   {result['r2']}")
        print(f"  Performance Metrics:")
        print(f"    Total time:     {result['total_time_ms']:.2f} ms")
        print(f"    Time/sample:    {result['time_per_sample_ms']:.4f} ms")
        print(f"    Throughput:     {result['throughput_samples_per_sec']:.0f} samples/sec")
        print(f"  Model size: {result['model_size_mb']:.3f} MB")
    
    # Save results
    output_file = model_dir / "benchmark_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to {output_file}")


if __name__ == "__main__":
    main()
