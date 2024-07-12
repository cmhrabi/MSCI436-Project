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
    cigarettesPerDay: '0',
    diabetes: false,
    hypertensive: false,
    bpMeds: false,
    totChol: 15,
    alcohol: false,
    sysBP: 15,
    stroke: false,
    diffWalking: false,
    glucose: '5',
    diaBP: '15',
    heartRate: '15',
  });
  const [output, setOutput] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [fetching, setFetching] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setInputs({
      ...inputs,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const confirmSubmission = window.confirm("Are you sure you want to submit?");
    if (!confirmSubmission) {
      return;
    }

    setFetching(true)

    const response = await fetch("http://localhost:5000/predict", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        model1: {
          BMI: inputs.BMI,
          smoking: inputs.smoking,
          alcohol: inputs.alcohol,
          stroke: inputs.stroke,
          diffWalking: inputs.diffWalking,
          sex: inputs.sex,
          age: inputs.age,
          race: inputs.race,
          diabetes: inputs.diabetes,
          geneticHealth: inputs.geneticHealth,
          asthma: inputs.asthma,
          kidney: inputs.kidney,
          skinCancer: inputs.skinCancer,
        },
        model2: {
          age: inputs.age,
          education: inputs.education,
          sex: inputs.sex,
          smoking: inputs.smoking,
          cigarettesPerDay: inputs.cigarettesPerDay,
          bpMeds: inputs.bpMeds,
          stroke: inputs.stroke,
          hypertensive: inputs.hypertensive,
          diabetes: inputs.diabetes,
          totChol: inputs.totChol,
          sysBP: inputs.sysBP,
          diaBP: inputs.diaBP,
          BMI: inputs.BMI,
          heartRate: inputs.heartRate,
          glucose: inputs.glucose,
        }})
    })

    try {
      if (response.ok) {
        const data = await response.json()

        const result = `
Does your patient have heart disease?
*${data.predict1[0] >= 0.5 ? "Yes" : "No"}

${data.predict1[0] < 0.5 ? `Is your patient at risk for heart disease in 10 years?
*${data.predict2[0] > 0.5 ? "Yes" : "No"}

${data.recommendations === 'NA' ? "No recommendations as you are not at Risk" : `Reduce patients BMI by: ${data.recommendations.BMI >0 ? data.recommendations.BMI : "Prediction does not change"}
Reduce patients total cholesterol by: ${data.recommendations.totChol >0 ? data.recommendations.totChol : "Prediction does not change" }
Quit smoking: ${data.recommendations.smoking ? "Yes" : "Prediction does not change"}`}` : `Your patient appears to have heart disease
please recommend treatment immediately`}
        `;
        setOutput(result);
        setIsModalOpen(true);
        setIsSubmitted(false);
        setFetching(false)
        setError('') // Reset the submission state
      } else {
        setFetching(false)
        if (response.status === 404) {
          setError('Server was not found, please ensure you have started the python API');
        } else if (response.status === 400) {
          setError('A bad request error occurred please validate inputs and try again')
        } else {
          setError('An error occurred please validate inputs and try again')
        }
      }
    } catch {
      setFetching(false)
      setError('An error occurred please validate inputs and try again')
    }
  };

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
            Difficulty Walking:
            <input
              type="checkbox"
              name="diffWalking"
              checked={inputs.diffWalking}
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
            Total Cholesterol:
            <input
              type="range"
              name="totChol"
              min="1"
              max="300"
              value={inputs.totChol}
              onChange={handleChange}
            />
            <span>{inputs.totChol}</span>
          </label>
        </div>
        <div className="form-group">
          <label>
            Systolic Blood Pressure:
            <input
              type="range"
              name="sysBP"
              min="0"
              max="300"
              value={inputs.sysBP}
              onChange={handleChange}
            />
            <span>{inputs.sysBP}</span>
          </label>
        </div>
        <div className="form-group">
          <label>
            Diastolic Blood Pressure:
            <input
              type="range"
              name="diaBP"
              min="0"
              max="150"
              value={inputs.diaBP}
              onChange={handleChange}
            />
            <span>{inputs.diaBP}</span>
          </label>
        </div>
        <div className="form-group">
          <label>
            Heart Rate:
            <input
              type="range"
              name="heartRate"
              min="0"
              max="150"
              value={inputs.heartRate}
              onChange={handleChange}
            />
            <span>{inputs.heartRate}</span>
          </label>
        </div>
        {error && <h2 className="error">{error}</h2>}
        <button type="submit">{fetching ? "Loading..." : "Submit"}</button>
      </form>
      <Modal
        isOpen={isModalOpen}
        onRequestClose={closeModal}
        contentLabel="Result Modal"
        className="Modal"
        overlayClassName="Overlay"
      >
        <div className="output-card">
          <h2>Results:</h2>
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
export default MainComponent;
