/**
 * Simulates a "heavy" app bundle that blocks the main thread for ~2.5–4 seconds.
 * Used in LCP demos: in "before", this runs in <head> and blocks parsing,
 * so the body (and hero image) aren't parsed until this finishes — bad LCP.
 */
(function () {
  var start = typeof performance !== 'undefined' ? performance.now() : 0;
  var n = 0;
  // Must be heavy enough that "before" LCP is clearly bad (>2.5s). ~100e6 ≈ same LCP as "after"; use 250e6+
  for (var i = 0; i < 250e6; i++) {
    n += Math.sqrt(i % 997) * Math.sin(i);
  }
  var elapsed = typeof performance !== 'undefined' ? (performance.now() - start).toFixed(2) : '?';
  console.log('[bundle.js] Simulated work done. Result:', n, 'Time:', elapsed, 'ms');
})();
