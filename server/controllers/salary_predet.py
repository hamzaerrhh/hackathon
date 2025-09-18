import pickle 

test_case = {  
    "years_experience": 5,
    "role": "Data Scientist",
    "degree": "Masters",
    "company_size": "Large",
    "location": "Casablanca",
    "level": "Senior"
}

# Save
with open("salary_prediction_model.pkl", "wb") as f:  
    pickle.dump(test_case, f)

# Load
with open("salary_prediction_model.pkl", "rb") as f:  
    loaded_data = pickle.load(f)

print(loaded_data)
