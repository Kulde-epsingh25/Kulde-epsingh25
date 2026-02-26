// Generate real logarithmic (golden) spiral
    const path = document.getElementById("spiralPath");

    const phi = (1 + Math.sqrt(5)) / 2;  // Golden ratio
    const b = Math.log(phi) / (Math.PI / 2); // Growth factor

    let points = "";
    let maxTheta = 7 * Math.PI; // Controls spiral length
    let step = 0.1;

    for (let theta = 0; theta < maxTheta; theta += step) {
      let r = Math.exp(b * theta);
      let x = r * Math.cos(theta);
      let y = r * Math.sin(theta);

      if (theta === 0)
        points += `M ${x} ${y}`;
      else
        points += ` L ${x} ${y}`;
    }

    path.setAttribute("d", points);