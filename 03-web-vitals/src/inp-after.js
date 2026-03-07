/**
 * INP — AFTER: Yield to main thread via setTimeout(0) and chunked processing.
 * UI updates (e.g. "Processing...") paint before the heavy work continues.
 */
(function () {
  var ITEMS = 10000;
  var CHUNK_SIZE = 500;
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

  function processNextChunk(dataArray, startIndex, chunkSize, callback) {
    var end = Math.min(startIndex + chunkSize, dataArray.length);
    for (var i = startIndex; i < end; i++) {
      doHeavyMath(dataArray[i]);
    }
    if (end < dataArray.length) {
      setTimeout(function () {
        processNextChunk(dataArray, end, chunkSize, callback);
      }, 0);
    } else {
      callback();
    }
  }

  btn.addEventListener('click', function () {
    status.textContent = '';
    btn.innerText = 'Processing...';

    // Yield: let the browser paint "Processing..." before starting heavy work
    setTimeout(function () {
      processNextChunk(data, 0, CHUNK_SIZE, function () {
        btn.innerText = 'Done!';
        status.textContent = 'Processed ' + ITEMS + ' items (chunked + yield).';
      });
    }, 0);
  });
})();
