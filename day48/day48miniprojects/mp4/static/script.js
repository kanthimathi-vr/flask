function drawTempChart(currentTemp) {
  const canvas = document.getElementById('tempChart');
  if (!canvas.getContext) return;
  const ctx = canvas.getContext('2d');

  // Dummy data: Temperatures throughout the day (in Celsius)
  const temps = [20, 22, 25, 28, currentTemp, 29, 27, 24, 22];
  const labels = ['6 AM', '8 AM', '10 AM', '12 PM', '2 PM', '4 PM', '6 PM', '8 PM', '10 PM'];

  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw axes
  ctx.beginPath();
  ctx.moveTo(50, 10);
  ctx.lineTo(50, 260);
  ctx.lineTo(580, 260);
  ctx.strokeStyle = '#555';
  ctx.lineWidth = 2;
  ctx.stroke();

  // Draw labels
  ctx.font = '12px Arial';
  ctx.fillStyle = '#333';
  labels.forEach((label, i) => {
    ctx.fillText(label, 50 + i * 60, 275);
  });

  // Draw temp line
  ctx.beginPath();
  temps.forEach((temp, i) => {
    const x = 50 + i * 60;
    const y = 260 - (temp * 6); // scale temp for canvas height
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.strokeStyle = '#ff6347';
  ctx.lineWidth = 3;
  ctx.stroke();

  // Draw points
  temps.forEach((temp, i) => {
    const x = 50 + i * 60;
    const y = 260 - (temp * 6);
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#ff6347';
    ctx.fill();

    ctx.fillStyle = '#000';
    ctx.fillText(temp + '°C', x - 15, y - 10);
  });
}
