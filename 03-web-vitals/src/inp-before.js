/**
 * INP — BEFORE: Blocking click handler.
 * Heavy work runs synchronously; the UI does not update until the loop finishes.
 */
(function () {
  var ITEMS = 10000;
  var data = [];
  for (var i = 0; i < ITEMS; i++) {
    data.push(Math.random() * 1000);
  }

  function doHeavyMath(x) {
    var n = 0;
    for (var i = 0; i < 1000; i++) {
      n += Math.sqrt(x + i) * Math.sin(i);
    }
    return n;
  }

  var btn = document.getElementById('process-btn');
  var status = document.getElementById('status');

  btn.addEventListener('click', function () {
    status.textContent = '';
    // UI update is queued but main thread is about to be blocked
    btn.innerText = 'Processing...';

    // Blocking: browser cannot paint until this finishes
    for (var i = 0; i < data.length; i++) {
      doHeavyMath(data[i]);
    }

    btn.innerText = 'Done!';
    status.textContent = 'Processed ' + ITEMS + ' items (blocking).';
  });
})();
