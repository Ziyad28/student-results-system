function confirmDelete() {
  return confirm("Are you sure you want to delete this student record?");
}

function gradeFromPercentage(percentage) {
  if (percentage >= 90) return "A+";
  if (percentage >= 80) return "A";
  if (percentage >= 70) return "B";
  if (percentage >= 60) return "C";
  if (percentage >= 50) return "D";
  return "F";
}

const form = document.getElementById("studentForm");
if (form) {
  const inputs = form.querySelectorAll('input[type="number"]');
  const totalEl = document.getElementById("previewTotal");
  const percentEl = document.getElementById("previewPercentage");
  const gradeEl = document.getElementById("previewGrade");

  function updatePreview() {
    let total = 0;
    inputs.forEach(input => {
      let value = Number(input.value || 0);
      if (value > 100) input.value = 100;
      if (value < 0) input.value = 0;
      total += Number(input.value || 0);
    });
    const percentage = (total / inputs.length).toFixed(2);
    totalEl.textContent = total;
    percentEl.textContent = percentage + "%";
    gradeEl.textContent = gradeFromPercentage(Number(percentage));
  }

  inputs.forEach(input => input.addEventListener("input", updatePreview));
  updatePreview();
}
