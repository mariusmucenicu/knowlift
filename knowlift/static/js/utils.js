// SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
// SPDX-License-Identifier: AGPL-3.0-or-later


function generateRandomNumber(upperBound, leftGlyph='(', rightGlyph=']', lowerBound=0) {
  /* the probability for rolling a correct answer is 100% for open & half-open intervals with the
   * same limits, i.e (2, 2) or [2, 2) will always yield 0 however there is only a 50% chance to
   * for the closed interval, i.e [2, 2] will yield either 0 or 1 (which is intended)
   * and the probability for the rest of the cases is 1/(upperBound + 1)
   */
  let openInterval = leftGlyph === '(' && rightGlyph === ')';
  let closedInterval = leftGlyph === '[' && rightGlyph === ']';

  if (openInterval) {
    upperBound = upperBound - 1;
  } else if (closedInterval) {
    upperBound = upperBound + 1;
  }

  let minimum = Math.ceil(lowerBound);
  let maximum = Math.floor(upperBound);
  return Math.floor(Math.random() * (maximum - minimum + 1)) + minimum;
}


function processFormData(btn) {
  let playForm = document.getElementById('play-form');
  let metaData = playForm.elements.metadata.value;
  let sendData = playForm.elements['play-form__input'];

  playForm.style.visibility = 'hidden';
  metaData = JSON.parse(metaData.replace(/'/g, '"'));

  if (btn.name === 'roulette') {
    let leftGlyph = metaData['left_glyph'];
    let rightGlyph = metaData['right_glyph'];
    let upperBound = metaData['stop_internal'] - metaData['start_internal'];
    metaData.answer = generateRandomNumber(upperBound, leftGlyph, rightGlyph);
  } else {
    metaData.answer = Number(sendData.value);
  }

  sendData.name = 'data';
  sendData.value = JSON.stringify(metaData);
}


function toggleBulkDisabled(items, state) {
  for (let i = 0; i < items.length; i++) {
    items[i].disabled = state;
  }
}


function checkEmptyInput(formInput) {
  let playFormButtons = document.querySelectorAll('.form-play__button--toggle');
  let timesGlyph = document.querySelector('.form-play__span--times');

  if (formInput.value) {
    timesGlyph.style.display = 'block';
    toggleBulkDisabled(playFormButtons, false);
  }
  else {
    timesGlyph.style.display = 'none';
    toggleBulkDisabled(playFormButtons, true);
  }
  
}


function clearFormField(clearSearchElement) {
  let playFormButtons = document.querySelectorAll('.form-play__button--toggle');
  let playForm = document.getElementById('play-form');
  let playFormInput = playForm.elements['play-form__input'];

  if (playFormInput.value) {
    playFormInput.value = '';
    playFormInput.focus();
    clearSearchElement.style.display = 'none';
    toggleBulkDisabled(playFormButtons, true);
  }
}


function fetchNavItems() {
  let drawerBackdrop = document.querySelector('#drawer-backdrop');
  let drawer = document.querySelector('.drawer');
  return [drawer, drawerBackdrop];
}


function openDrawer() {
  let [drawer, drawerBackdrop] = fetchNavItems();
  drawer.classList.add('open');
  drawerBackdrop.classList.add('backdrop');
}


function closeDrawer() {
  let [drawer, drawerBackdrop] = fetchNavItems();
  drawer.classList.remove('open');
  drawerBackdrop.classList.remove('backdrop');
}


function scrollToElement(targetID) {
  let targetElement = document.getElementById(targetID);
  let scrollIntoViewOptions = {behavior: 'smooth', block: 'start'};
  targetElement.scrollIntoView(scrollIntoViewOptions);
}
