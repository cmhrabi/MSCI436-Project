import React, { useState } from 'react';
import Modal from 'react-modal';
import './index.css';
import heart from './heart.png';

Modal.setAppElement('#root'); // Ensure this line is present to avoid accessibility issues

const MainComponent = () => {
  const [inputs, setInputs] = useState({
    age: '',
    race: '5',
    education: '1',
    sex: 'M',
    geneticHealth: '1',
    asthma: false,
    kidney: false,
    skinCancer: false,
    BMI: 28.4,
    smoking: false,
    cigarettesPerDay: '',
    diabetes: false,
    hypertensive: false,
    bpMeds: false,
    physicalHealth: 15,
    alcohol: false,
    mentalHealth: 15,
    stroke: false,
    glucose: '',
  });
  const [output, setOutput] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setInputs({
      ...inputs,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const [sampleData, setSampleData] = useState({
    age: 64,
    education: 2,
    sex: 1,
    is_smoking: 1,
    cigs_per_day: 3,
    BP_meds: 0,
    prevalent_stroke: 0,
    prevalent_hyp: 0,
    diabetes: 0,
    tot_chol: 221,
    sys_BP: 148,
    dia_BP: 85,
    bmi: 29.77,
    heart_rate: 90,
    glucose: 80
  });

  const handleSubmit = async (event) => {
    event.preventDefault();
    const confirmSubmission = window.confirm("Are you sure you want to submit?");
    if (!confirmSubmission) {
      return;
    }

    fetch("http://localhost:5000/predict", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(sampleData)
    })
    .then(response => response.json())
    .then(data => {
      // Mock output values
      const heartDisease = "Yes";
      const reduceCigarettes = 4;
      const increasePhysicalHealth = 10;
      const riskHeartDisease = "Yes"

      const result = `
        Do you have heart disease?
        *${heartDisease}

        Are you at risk for heart disease in 10 years?
        *${riskHeartDisease}

      Reduce Cigarettes/Day by: *${reduceCigarettes}
      Minimize Alcohol Drinking
      Increase Physical Health by: *${increasePhysicalHealth}
    `;
    setOutput(result);
    setIsModalOpen(true);
    setIsSubmitted(false); // Reset the submission state
    });

  const handleDoctorConfirm = () => {
    setIsSubmitted(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="main-container">
      <div className="header">
        <img src={heart} alt="Heart" />
        <h1>Risk of Heart Disease</h1>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>
            Age:
            <input
              type="number"
              name="age"
              value={inputs.age}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Race:
            <select
              name="race"
              value={inputs.race}
              onChange={handleChange}
            >
              <option value="1">Other</option>
              <option value="2">Hispanic</option>
              <option value="3">Asian</option>
              <option value="4">Black</option>
              <option value="5">White</option>
            </select>
          </label>
        </div>
        <div className="form-group">
          <label>
            Education Level:
            <select
              name="education"
              value={inputs.education}
              onChange={handleChange}
            >
              <option value="1">Dropout</option>
              <option value="2">Highschool</option>
              <option value="3">Undergrad</option>
              <option value="4">Master</option>
            </select>
          </label>
        </div>
        <div className="form-group">
          <label>
            Sex:
            <select
              name="sex"
              value={inputs.sex}
              onChange={handleChange}
            >
              <option value="M">M</option>
              <option value="F">F</option>
            </select>
          </label>
        </div>
        <div className="form-group">
          <label>
            Genetic Health:
            <select
              name="geneticHealth"
              value={inputs.geneticHealth}
              onChange={handleChange}
            >
              <option value="1">Excellent</option>
              <option value="2">Very Good</option>
              <option value="3">Good</option>
              <option value="4">Fair</option>
              <option value="5">Poor</option>
            </select>
          </label>
        </div>
        <div className="form-group">
          <label>
            Smoking:
            <input
              type="checkbox"
              name="smoking"
              checked={inputs.smoking}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Glucose Level:
            <input
              type="number"
              name="glucose"
              value={inputs.glucose}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Cigarettes per day:
            <input
              type="number"
              name="cigarettesPerDay"
              value={inputs.cigarettesPerDay}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Diabetes:
            <input
              type="checkbox"
              name="diabetes"
              checked={inputs.diabetes}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Hypertensive:
            <input
              type="checkbox"
              name="hypertensive"
              checked={inputs.hypertensive}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Blood Pressure Medications:
            <input
              type="checkbox"
              name="bpMeds"
              checked={inputs.bpMeds}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Asthma:
            <input
              type="checkbox"
              name="asthma"
              checked={inputs.asthma}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Kidney Disease:
            <input
              type="checkbox"
              name="kidney"
              checked={inputs.kidney}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Skin Cancer:
            <input
              type="checkbox"
              name="skinCancer"
              checked={inputs.skinCancer}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Stroke:
            <input
              type="checkbox"
              name="stroke"
              checked={inputs.stroke}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            Alcohol:
            <input
              type="checkbox"
              name="alcohol"
              checked={inputs.alcohol}
              onChange={handleChange}
            />
          </label>
        </div>
        <div className="form-group">
          <label>
            BMI:
            <input
              type="range"
              name="BMI"
              min="1"
              max="56.8"
              value={inputs.BMI}
              onChange={handleChange}
            />
            <span>{inputs.BMI}</span>
          </label>
        </div>
        <div className="form-group">
          <label>
            Physical Health:
            <input
              type="range"
              name="physicalHealth"
              min="1"
              max="30"
              value={inputs.physicalHealth}
              onChange={handleChange}
            />
            <span>{inputs.physicalHealth}</span>
          </label>
        </div>
        <div className="form-group">
          <label>
            Mental Health:
            <input
              type="range"
              name="mentalHealth"
              min="0"
              max="30"
              value={inputs.mentalHealth}
              onChange={handleChange}
            />
            <span>{inputs.mentalHealth}</span>
          </label>
        </div>
        <button type="submit">Submit</button>
      </form>
      <Modal
        isOpen={isModalOpen}
        onRequestClose={closeModal}
        contentLabel="Result Modal"
        className="Modal"
        overlayClassName="Overlay"
      >
        <div className="output-card">
          <h2>Output:</h2>
          <pre>{output}</pre>
          {!isSubmitted && <button onClick={handleDoctorConfirm}>Confirm Diagnosis</button>}
          {isSubmitted && <p>The diagnosis has been submitted to the database.</p>}
          <div></div>
          <button onClick={closeModal}>Close</button>
        </div>
      </Modal>
    </div>
  );
};
}
export default MainComponent;
