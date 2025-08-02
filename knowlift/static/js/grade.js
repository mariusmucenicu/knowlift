// SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
// SPDX-License-Identifier: AGPL-3.0-or-later


function validateForm(event) {
    const isRadioChecked = document.querySelector('input:checked') !== null;
    const choiceBtn = document.querySelector('#js-btn-choice');

    if (isRadioChecked && choiceBtn.disabled) {
        choiceBtn.disabled = false;
    } else if (event.target.id === 'js-btn-random') {
        const choices = document.querySelectorAll('input');
        const randomChoice = Math.floor(Math.random() * 4);
        const choice = choices[randomChoice];
        choice.checked = true;
    }
}

const gradeForm = document.getElementById('levels');
gradeForm.addEventListener('click', validateForm);
