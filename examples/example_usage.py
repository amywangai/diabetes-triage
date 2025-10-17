"""
Example usage of the diabetes progression prediction API.
"""
import requests
import json


def main():
    """Demonstrate API usage."""
    base_url = "http://localhost:8000"
    
    # 1. Check API health
    print("1. Checking API health...")
    response = requests.get(f"{base_url}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    
    # 2. Make a single prediction
    print("2. Making a prediction...")
    patient_data = {
        "age": 0.02,
        "sex": -0.044,
        "bmi": 0.06,
        "bp": -0.03,
        "s1": -0.02,
        "s2": 0.03,
        "s3": -0.02,
        "s4": 0.02,
        "s5": 0.02,
        "s6": -0.001
    }
    
    response = requests.post(f"{base_url}/predict", json=patient_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    
    # 3. Batch predictions for multiple patients
    print("3. Making batch predictions...")
    patients = [
        {
            "id": "patient_001",
            "data": {
                "age": 0.05, "sex": 0.05, "bmi": 0.08, "bp": 0.02,
                "s1": 0.01, "s2": 0.04, "s3": -0.01, "s4": 0.03,
                "s5": 0.05, "s6": 0.02
            }
        },
        {
            "id": "patient_002",
            "data": {
                "age": -0.03, "sex": -0.04, "bmi": -0.02, "bp": -0.05,
                "s1": -0.03, "s2": -0.01, "s3": 0.02, "s4": -0.02,
                "s5": -0.03, "s6": -0.04
            }
        },
        {
            "id": "patient_003",
            "data": {
                "age": 0.08, "sex": 0.05, "bmi": 0.12, "bp": 0.08,
                "s1": 0.05, "s2": 0.07, "s3": -0.05, "s4": 0.06,
                "s5": 0.09, "s6": 0.05
            }
        }
    ]
    
    results = []
    for patient in patients:
        response = requests.post(f"{base_url}/predict", json=patient["data"])
        result = response.json()
        results.append({
            "patient_id": patient["id"],
            "prediction": result["prediction"],
            "model_version": result["model_version"]
        })
    
    # Sort by risk (descending)
    results.sort(key=lambda x: x["prediction"], reverse=True)
    
    print("   Patients sorted by progression risk (high to low):")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['patient_id']}: {result['prediction']:.2f}")
    
    print("\n   ⚠️  Patient {} should be prioritized for follow-up".format(
        results[0]['patient_id']
    ))
    
    # 4. Test error handling
    print("\n4. Testing error handling with invalid input...")
    invalid_data = {"age": 0.02}  # Missing required fields
    response = requests.post(f"{base_url}/predict", json=invalid_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    main()
