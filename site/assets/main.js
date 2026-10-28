(function () {
  // ---------------------------------------------------------------- mobilmeny
  var nav = document.querySelector('.nav');
  var burger = document.querySelector('.burger');
  if (nav && burger) {
    var close = function () { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); };
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { close(); burger.focus(); }
    });
    nav.querySelectorAll('.menu a').forEach(function (a) { a.addEventListener('click', close); });
  }

  // ---------------------------------------------------------------- kontaktformulär
  // Utan formulärtjänst öppnas ett ifyllt mejl till mail@nykael.se.
  // Sätt data-endpoint på <form> (t.ex. en Formspree-adress) så skickas formuläret direkt i stället.
  var form = document.getElementById('kontaktform');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.msg');
      var d = new FormData(form);
      var val = function (k) { return (d.get(k) || '').toString().trim(); };
      if (!val('namn') || !val('meddelande') || (!val('epost') && !val('telefon'))) {
        msg.setAttribute('data-err', '');
        msg.textContent = 'Fyll i namn, meddelande och e-post eller telefon så att vi kan svara er.';
        return;
      }
      msg.removeAttribute('data-err');
      var to = form.getAttribute('data-to');
      var endpoint = form.getAttribute('data-endpoint');
      if (endpoint) {
        msg.textContent = 'Skickar…';
        fetch(endpoint, { method: 'POST', body: d, headers: { Accept: 'application/json' } })
          .then(function (r) {
            if (!r.ok) throw new Error(r.status);
            form.reset();
            msg.textContent = 'Tack! Vi har tagit emot ert meddelande och återkommer så snart vi kan.';
          })
          .catch(function () {
            msg.setAttribute('data-err', '');
            msg.textContent = 'Meddelandet kunde inte skickas. Ring 031-80 13 50 eller mejla ' + to + '.';
          });
        return;
      }
      var body = 'Namn: ' + val('namn') + '\nFöretag: ' + val('foretag') + '\nE-post: ' + val('epost') +
        '\nTelefon: ' + val('telefon') + '\nÄrende: ' + val('arende') + '\n\n' + val('meddelande');
      msg.textContent = 'Ert e-postprogram öppnas med meddelandet ifyllt. Öppnas inget? Mejla ' + to + ' eller ring 031-80 13 50.';
      window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent('Förfrågan: ' + val('arende')) + '&body=' + encodeURIComponent(body);
    });
  }
})();
