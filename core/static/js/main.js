document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open);
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Fade-in on scroll. Content stays visible if JS or IntersectionObserver is missing.
  var revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length && "IntersectionObserver" in window) {
    document.documentElement.classList.add("reveal-ready");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  // Set up location fields first so their validity is ready for the checks below.
  document
    .querySelectorAll("input[data-location-autocomplete]")
    .forEach(setupLocationInput);

  // Registration form: green border once a field is filled in correctly.
  // (The phone field has its own live check on the register page.)
  var donorForm = document.querySelector("form.donor-form");
  if (donorForm) {
    var fields = donorForm.querySelectorAll("input, select");
    var markField = function (el) {
      if (el.type === "hidden" || el.hasAttribute("data-phone")) return;
      var filled = el.value.trim() !== "";
      el.classList.toggle("valid", filled && el.checkValidity());
      el.classList.toggle("invalid", filled && !el.checkValidity());
    };
    fields.forEach(function (el) {
      ["input", "change", "blur"].forEach(function (evt) {
        el.addEventListener(evt, function () { markField(el); });
      });
      markField(el);
    });
  }

  var form = document.querySelector("form[data-confirm]");
  if (form) {
    form.addEventListener("submit", function (e) {
      if (!window.confirm(form.dataset.confirm)) {
        e.preventDefault();
      }
    });
  }

  var searchForm = document.querySelector("form.filters");
  if (searchForm) {
    var locationInput = searchForm.querySelector("#location");
    var results = document.getElementById("results");
    var lastQuery = null;
    var searchTimer = null;
    var searchId = 0;

    function currentQuery() {
      var params = new URLSearchParams();
      var group = searchForm.querySelector("#blood_group").value;
      var loc = locationInput ? locationInput.value.trim() : "";
      if (group) params.set("blood_group", group);
      if (loc) params.set("location", loc);
      return params.toString();
    }

    lastQuery = currentQuery();

    // Re-run the search in place so typing focus isn't lost.
    function runSearch() {
      var query = currentQuery();
      if (query === lastQuery || !results) return;
      lastQuery = query;
      var id = ++searchId;
      var url = window.location.pathname + (query ? "?" + query : "");
      fetch(url, { headers: { "X-Requested-With": "fetch" } })
        .then(function (r) { return r.text(); })
        .then(function (html) {
          if (id !== searchId) return;
          var doc = new DOMParser().parseFromString(html, "text/html");
          var fresh = doc.getElementById("results");
          if (fresh) results.innerHTML = fresh.innerHTML;
          window.history.replaceState(null, "", url);
        })
        .catch(function () { searchForm.submit(); });
    }

    searchForm.querySelector("#blood_group").addEventListener("change", runSearch);

    if (locationInput) {
      locationInput.addEventListener("input", function () {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(runSearch, 500);
      });
      // Fired when a suggestion is picked or "use my location" fills the field.
      locationInput.addEventListener("change", function () {
        clearTimeout(searchTimer);
        runSearch();
      });
    }

    searchForm.addEventListener("submit", function (e) {
      if (locationInput) {
        locationInput.value = locationInput.value.trim();
      }
    });
  }

  // Contact button: show the donor's number with call / copy options.
  var contactPop = null;
  var contactBtn = null;

  function closeContactPop() {
    if (contactPop) contactPop.hidden = true;
    if (contactBtn) contactBtn.setAttribute("aria-expanded", "false");
    contactPop = null;
    contactBtn = null;
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy") ? resolve() : reject(new Error("copy failed"));
      } catch (err) {
        reject(err);
      }
      document.body.removeChild(ta);
    });
  }

  function openContactPop(btn) {
    var phone = (btn.getAttribute("data-contact-phone") || "").trim();
    if (!phone) return;

    if (!contactPop) {
      contactPop = document.createElement("div");
      contactPop.className = "contact-pop";
      contactPop.setAttribute("role", "dialog");
      contactPop.setAttribute("aria-label", "Contact options");
      document.body.appendChild(contactPop);
    }

    contactPop.innerHTML =
      '<span class="contact-pop-label">Contact Number</span>' +
      '<a class="contact-pop-number" href="tel:' + phone.replace(/[^\d+]/g, "") + '">' + phone + "</a>" +
      '<div class="contact-pop-actions">' +
        '<a class="btn-red contact-pop-call" href="tel:' + phone.replace(/[^\d+]/g, "") + '">' +
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>' +
          "Call Now</a>" +
        '<button type="button" class="btn-outline contact-pop-copy">' +
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16 1H4a2 2 0 0 0-2 2v14h2V3h12V1zm3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm0 16H8V7h11v14z"/></svg>' +
          "<span>Copy Number</span></button>" +
      "</div>";

    contactBtn = btn;
    btn.setAttribute("aria-expanded", "true");
    contactPop.hidden = false;

    var rect = btn.getBoundingClientRect();
    var pop = contactPop;
    pop.style.left = "0px";
    pop.style.top = "0px";
    var w = pop.offsetWidth;
    var h = pop.offsetHeight;
    var left = Math.min(Math.max(8, rect.right - w), window.innerWidth - w - 8);
    var top = rect.bottom + 8;
    if (top + h > window.innerHeight - 8) top = Math.max(8, rect.top - h - 8);
    pop.style.left = Math.round(left) + "px";
    pop.style.top = Math.round(top) + "px";

    var copyBtn = pop.querySelector(".contact-pop-copy");
    copyBtn.addEventListener("click", function () {
      copyText(phone).then(function () {
        copyBtn.classList.add("copied");
        copyBtn.querySelector("span").textContent = "Copied!";
        setTimeout(closeContactPop, 900);
      }).catch(function () {
        copyBtn.querySelector("span").textContent = "Copy failed";
        setTimeout(function () {
          if (copyBtn.querySelector("span")) copyBtn.querySelector("span").textContent = "Copy Number";
        }, 1500);
      });
    });
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest ? e.target.closest("[data-contact-phone]") : null;
    if (btn) {
      e.preventDefault();
      if (contactBtn === btn) { closeContactPop(); return; }
      closeContactPop();
      openContactPop(btn);
      return;
    }
    if (contactPop && !contactPop.contains(e.target)) closeContactPop();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeContactPop();
  });

  window.addEventListener("scroll", closeContactPop, true);
  window.addEventListener("resize", closeContactPop);
});

/* ---------------------------------------------------------
   Location autocomplete (Photon / OpenStreetMap, no API key)
   data-location-autocomplete="full"  -> "Kaloor, Ernakulam, Kerala"
   data-location-autocomplete="short" -> "Kaloor" (matches stored text)
--------------------------------------------------------- */
var PHOTON_URL = "https://photon.komoot.io";

function placeLabel(props, mode) {
  var area = props.name || props.street || props.city || props.county || "";
  if (mode === "short") {
    return area;
  }
  var parts = [area, props.district || props.city || props.county, props.state];
  return parts
    .filter(function (p, i) { return p && parts.indexOf(p) === i; })
    .join(", ");
}

function setupLocationInput(input) {
  var mode = input.dataset.locationAutocomplete;
  input.setAttribute("autocomplete", "off");

  var wrap = document.createElement("div");
  wrap.className = "location-wrap";
  input.parentNode.insertBefore(wrap, input);
  wrap.appendChild(input);

  var locate = document.createElement("button");
  locate.type = "button";
  locate.className = "locate-btn";
  locate.title = "Use my current location";
  locate.setAttribute("aria-label", "Use my current location");
  locate.innerHTML =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm8.9 3A9 9 0 0 0 13 3.1V1h-2v2.1A9 9 0 0 0 3.1 11H1v2h2.1A9 9 0 0 0 11 20.9V23h2v-2.1a9 9 0 0 0 7.9-7.9H23v-2h-2.1zM12 19a7 7 0 1 1 0-14 7 7 0 0 1 0 14z"/></svg>';
  wrap.appendChild(locate);

  var list = document.createElement("ul");
  list.className = "location-suggestions";
  list.hidden = true;
  wrap.appendChild(list);

  // On the registration form the location must be chosen from the suggestions
  // (or the "use my location" button), not typed freehand.
  var requirePick = mode === "full";
  var picked = input.value.trim(); // a value restored after a server error counts as picked
  var pickMessage = null;
  var touched = false;

  if (requirePick) {
    pickMessage = document.createElement("p");
    pickMessage.className = "phone-status bad";
    pickMessage.setAttribute("aria-live", "polite");
    wrap.insertAdjacentElement("afterend", pickMessage);
  }

  function syncPick() {
    if (!requirePick) return;
    var value = input.value.trim();
    var ok = value === "" || value === picked;
    input.setCustomValidity(ok ? "" : "Select a place from the suggestions");
    pickMessage.textContent = ok || !touched ? "" : "Select a place from the suggestions";
  }

  function setPicked(value) {
    picked = value;
    input.value = value;
    input.dispatchEvent(new Event("change"));
  }

  input.addEventListener("input", syncPick);
  input.addEventListener("change", syncPick);
  input.addEventListener("blur", function () { touched = true; syncPick(); });
  input.addEventListener("invalid", function () { touched = true; syncPick(); });
  syncPick();

  var timer = null;
  var requestId = 0;

  function hide() { list.hidden = true; list.innerHTML = ""; }

  function show(features) {
    list.innerHTML = "";
    var seen = {};
    features.forEach(function (f) {
      var label = placeLabel(f.properties, mode);
      if (!label || seen[label]) return;
      seen[label] = true;
      var li = document.createElement("li");
      li.textContent = placeLabel(f.properties, "full") || label;
      li.addEventListener("mousedown", function (e) {
        e.preventDefault();
        hide();
        setPicked(label);
      });
      list.appendChild(li);
    });
    list.hidden = !list.children.length;
  }

  input.addEventListener("input", function () {
    clearTimeout(timer);
    var q = input.value.trim();
    if (q.length < 3) { hide(); return; }
    timer = setTimeout(function () {
      var id = ++requestId;
      fetch(PHOTON_URL + "/api/?limit=6&lang=en&q=" + encodeURIComponent(q))
        .then(function (r) { return r.json(); })
        .then(function (data) { if (id === requestId) show(data.features || []); })
        .catch(hide);
    }, 350);
  });

  input.addEventListener("blur", hide);
  input.addEventListener("keydown", function (e) {
    if (e.key === "Escape") hide();
  });

  locate.addEventListener("click", function () {
    if (!navigator.geolocation) {
      window.alert("Location is not supported by this browser.");
      return;
    }
    locate.classList.add("busy");
    navigator.geolocation.getCurrentPosition(
      function (pos) {
        var url = PHOTON_URL + "/reverse?lang=en&lat=" + pos.coords.latitude +
          "&lon=" + pos.coords.longitude;
        fetch(url)
          .then(function (r) { return r.json(); })
          .then(function (data) {
            var f = (data.features || [])[0];
            if (f) setPicked(placeLabel(f.properties, mode));
          })
          .catch(function () { window.alert("Could not look up your location."); })
          .then(function () { locate.classList.remove("busy"); });
      },
      function () {
        locate.classList.remove("busy");
        window.alert("Unable to get your location. Please allow location access or type it in.");
      },
      { timeout: 10000 }
    );
  });
}
