(function () {
  const html = document.documentElement;
  const jsonPath =
    html.getAttribute('data-lp-json') ||
    (function () {
      const m = location.pathname.match(/\/([a-z-]+)\/(?:fresh-air-pro\/)?landing(?:-[0-9]+)?\.html$/);
      return m ? '/content/it/products/' + m[1] + '/landing.json' : '';
    })();

  if (!jsonPath) return;

  function get(obj, path) {
    return path.split('.').reduce(function (acc, key) {
      if (acc == null) return undefined;
      return acc[key];
    }, obj);
  }

  function setText(sel, value) {
    const el = document.querySelector(sel);
    if (el && value != null) el.textContent = value;
  }

  function setHtml(sel, value) {
    const el = document.querySelector(sel);
    if (el && value != null) el.innerHTML = value;
  }

  function apply(data) {
    if (!data) return;

    document.title = data.meta?.title || document.title;
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc && data.meta?.description) metaDesc.setAttribute('content', data.meta.description);

    setText('.banner-urgency__main', data.banner_urgency?.main);
    setText('.hero-headline__rating span:last-child', data.headline?.rating_label);
    setHtml('.hero-headline__title', data.headline?.title);
    setText('.hero-headline__subtitle', data.headline?.subtitle);

    const heroImg = document.querySelector('.hero-headline__image img');
    if (heroImg && data.headline?.image_alt) heroImg.alt = data.headline.image_alt;

    setText('.price-discount__label', data.price?.label);
    const oldPrice = document.querySelector('.price-discount .price-anchor__old');
    const newPrice = document.querySelector('.price-discount .price-anchor__new');
    const discount = document.querySelector('.price-discount .price-anchor__discount');
    if (oldPrice && data.price?.anchor) oldPrice.textContent = data.price.anchor + ' ' + (data.price.currency || '€');
    if (newPrice && data.price?.final) newPrice.textContent = data.price.final + ' ' + (data.price.currency || '€');
    if (discount && data.price?.discount) discount.textContent = data.price.discount;

    document.querySelectorAll('.bullet-list-checkmark li').forEach(function (li, i) {
      const bullet = data.bullets?.[i];
      if (bullet?.text) {
        li.innerHTML = bullet.text;
        li.hidden = false;
      } else {
        li.remove();
      }
    });

    document.querySelectorAll('.form-1 .cod-form__title').forEach(function (el) {
      if (data.form?.title) el.textContent = data.form.title;
    });
    document.querySelectorAll('.form-1 .cod-form__subtitle').forEach(function (el) {
      if (data.form?.subtitle) el.textContent = data.form.subtitle;
    });
    document.querySelectorAll('.form-2 .cod-form__title').forEach(function (el) {
      if (data.form?.title) el.textContent = data.form.title;
    });
    document.querySelectorAll('.form-2 .cod-form__subtitle').forEach(function (el) {
      if (data.form?.subtitle) el.textContent = data.form.subtitle;
    });

    const ctaButtons = document.querySelectorAll('.cod-form .cta-button');
    ctaButtons.forEach(function (btn) {
      if (data.form?.cta_button) btn.textContent = data.form.cta_button;
    });

    if (data.macro_review) {
      setText('.macro-review__quote', data.macro_review.quote);
      setText('.macro-review__author', data.macro_review.author);
      setText('.macro-review__credentials', data.macro_review.credentials);
      setText('.macro-review__stars', data.macro_review.stars);
    }

    if (data.competitor_destruction) {
      setText('.competitor-destruction .section__title', data.competitor_destruction.title);
      setText('.competitor-destruction .section__subtitle', data.competitor_destruction.subtitle);
      document.querySelectorAll('.competitor-table tbody tr').forEach(function (row, i) {
        const item = data.competitor_destruction.rows?.[i];
        if (!item) return;
        const cells = row.querySelectorAll('td');
        if (cells[0] && item.bad) cells[0].textContent = item.bad;
        if (cells[1] && item.good) cells[1].textContent = item.good;
      });
    }

    document.querySelectorAll('.reviews-grid__list .review-card').forEach(function (card, i) {
      const review = data.reviews?.[i];
      if (!review) return;
      setText(card.querySelector('.review-card__name'), review.name);
      setText(card.querySelector('.review-card__location'), review.location);
      setText(card.querySelector('.review-card__stars'), review.stars);
      setText(card.querySelector('.review-card__title'), review.title);
      setText(card.querySelector('.review-card__text'), review.text);
    });

    if (data.package_content) {
      setText('.package-content .section__title', data.package_content.title);
      setText('.package-content .section__subtitle', data.package_content.subtitle);
      document.querySelectorAll('.package-content__list li').forEach(function (li, i) {
        const item = data.package_content.items?.[i];
        if (item?.text) li.innerHTML = item.text;
      });
    }

    if (data.incentive_2) {
      setText('.incentive-badges-2 h2', data.incentive_2.title);
      setHtml('.incentive-badges-2 p', data.incentive_2.text);
    }

    if (data.faq) {
      setText('.faq .section__title', data.faq.title);
      document.querySelectorAll('.faq details').forEach(function (detail, i) {
        const item = data.faq.items?.[i];
        if (!item) return;
        const summary = detail.querySelector('summary');
        const body = detail.querySelector('.faq-accordion__body');
        if (summary) summary.textContent = item.q;
        if (body) body.innerHTML = item.a;
      });
    }

    if (data.meta?.price && window.SITE_CONFIG) {
      window.SITE_CONFIG.PRICE = parseFloat(data.meta.price);
    }
  }

  function loadFromNetwork() {
    return fetch(jsonPath, { cache: 'no-store' }).then(function (res) {
      if (!res.ok) throw new Error('JSON non trovato');
      return res.json();
    });
  }

  window.addEventListener('message', function (event) {
    if (event.data && event.data.type === 'lp-preview' && event.data.payload) {
      apply(event.data.payload);
    }
  });

  loadFromNetwork()
    .then(apply)
    .catch(function () {
      /* static HTML fallback */
    });
})();
