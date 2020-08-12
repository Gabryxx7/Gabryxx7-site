!function (window, document) {
  var LM = 'light-mode';
  var DM = 'dark-mode';
  var h = new Date().getHours();
  document.body.classList.add(DM); /*Start in dark mode and eventually switch */
  console.log("match_os " + match_os + " time " +h);
  /* if match_os is false, the time has the preference on deciding  which mode */
  if (window.match_os  && 'matchMedia' in window && window.matchMedia('(prefers-color-scheme)')) return;
  var m = h <= window._sunrise || h >= window._sunset  ? DM : LM; 
  var n = m === DM ? LM : DM;
  document.body.classList.add(m);
  document.body.classList.remove(n);
}(window, document);
