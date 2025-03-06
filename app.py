from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Load knowledge base
with open("static/knowledge_base.json", "r") as file:
    knowledge_base = json.load(file)


@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.get_json()
    user_symptoms = set(data.get("symptoms", []))

    if not user_symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    diagnosis_results = []

    # Calculate confidence scores for each disease
    for disease, details in knowledge_base.items():
        disease_symptoms = set(details["symptoms"])
        match_count = len(user_symptoms & disease_symptoms)

        if match_count > 0:
            confidence_score = (match_count / len(disease_symptoms)) * 100  # Percentage match
            diagnosis_results.append({
                "disease": disease,
                "confidence": round(confidence_score, 2),
                "symptoms": details["symptoms"],
                "description": details["description"],
                "treatment": details["treatment"]
            })

    # Sort by confidence score (highest first)
    diagnosis_results.sort(key=lambda x: x["confidence"], reverse=True)

    # Only return top 3 results
    diagnosis_results = diagnosis_results[:3]  # Limit to top 3 results for simplicity

    if diagnosis_results:
        # Return results as JSON
        return jsonify(diagnosis_results)
    else:
        return jsonify({"message": "No strong match found. Please consult a doctor."})


@app.route('/')
def index():
    return render_template("main.html")

if __name__ == '__main__':
    app.run(debug=True)




