const buttons = document.querySelectorAll(".btn");

const result = document.getElementById("result");

buttons.forEach(button => {

  button.addEventListener("click", async () => {

    if (button.id === "clear-btn") {

      result.innerHTML = `
        <p class="placeholder">
          Нажми кнопку слева ✨
        </p>
      `;

      return;
    }

    const url = button.dataset.url;

    result.innerHTML = `
      <p class="placeholder">
        Загрузка...
      </p>
    `;

    try {

      const response = await fetch(url);

      const data = await response.json();

      result.innerHTML = `
        <div class="card">

          <h2>${data.label}</h2>

          <div class="value">
            ${data.value}
          </div>

        </div>
      `;

    } catch (error) {

      result.innerHTML = `
        <p style="color:red;">
          Ошибка сервера 😭
        </p>
      `;
    }

  });

});