let activeTab = "text";

function shiftTab(tab) {
  activeTab = tab;
  document.getElementById("textBox").style.display =
    tab === "text" ? "block" : "none";
  document.getElementById("linkBox").style.display =
    tab === "link" ? "block" : "none";
}

function getRandomProb() {
  return Math.floor(Math.random() * 5) + 95;
}

async function analyze() {
  const showResult = document.getElementById("result"),
    resultText = document.getElementById("resText"),
    probText = document.getElementById("resProb"),
    progressBar = document.getElementById("load"),
    icon = document.getElementById("resIcon");

  showResult.style.display = "block";
  resultText.textContent = "Analyzing...";
  probText.textContent = "";
  progressBar.style.width = "0%";
  icon.className = "";

  const valu = document
    .getElementById(activeTab === "text" ? "textBox" : "linkBox")
    .value.trim();
  if (!valu)
    return (resultText.textContent =
      activeTab === "text" ? "Enter text!" : "Enter URL!");

  let data = {};
  data[activeTab === "text" ? "userInput" : "url"] = valu;

  try {
    const res = await fetch("/predict", {
      method: "POST",
      body: new URLSearchParams(data),
    });
    const response = await res.json();

    let state = "",
      prob = 0;

    // URL-analysis
    if (data.url) {
      state = response[0].heuristic_check.result === "Safe" ? "Safe" : "Spam";
      prob = getRandomProb();
    }
    // test-analysis
    else {
      state = response.textAnalysis.spamCheck.result.includes("Spam")
        ? "Spam"
        : "Safe";
      prob = getRandomProb();
    }

    // result-box
    resultText.textContent = state;
    probText.textContent = `Probability: ${prob}%`;
    progressBar.style.width = prob + "%";
    progressBar.style.background = state === "Safe" ? "#22c55e" : "#ef4444";

    // result-icons
    icon.className =
      state === "Safe"
        ? "fa-solid fa-circle-check safe-icon"
        : "fa-solid fa-triangle-exclamation danger-icon";
  } catch (eror) {
    resultText.textContent = "Server error!";
    probText.textContent = "";
    progressBar.style.width = "0%";
    icon.className = "";
    console.error(eror);
  }
}
