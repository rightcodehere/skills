# CSS / Less / Sass Review Guide

CSS ，、、。

## CSS  vs 

### 

```css
/* ❌  -  */
.button {
  background: #3b82f6;
  border-radius: 8px;
}
.card {
  border: 1px solid #3b82f6;
  border-radius: 8px;
}

/* ✅  CSS  */
:root {
  --color-primary: #3b82f6;
  --radius-md: 8px;
}
.button {
  background: var(--color-primary);
  border-radius: var(--radius-md);
}
.card {
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
}
```

### 

```css
/*  */
:root {
  /*  */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-text: #1f2937;
  --color-text-muted: #6b7280;
  --color-bg: #ffffff;
  --color-border: #e5e7eb;

  /*  */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /*  */
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 18px;
  --font-weight-normal: 400;
  --font-weight-bold: 700;

  /*  */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /*  */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);

  /*  */
  --transition-fast: 150ms ease;
  --transition-normal: 300ms ease;
}
```

### 

```css
/* ✅  -  */
.card {
  --card-padding: var(--spacing-md);
  --card-radius: var(--radius-md);

  padding: var(--card-padding);
  border-radius: var(--card-radius);
}

/* ⚠️  JS  -  */
```

### 

- [ ] ？
- [ ] ？
- [ ] ？
- [ ] ？

---

## !important 

### 

```css
/* ✅  -  */
.hidden { display: none !important; }
.sr-only { position: absolute !important; }

/* ✅ （） */
.third-party-modal {
  z-index: 9999 !important;
}

/* ✅  */
@media print {
  .no-print { display: none !important; }
}
```

### 

```css
/* ❌  -  */
.button {
  background: blue !important;  /*  !important? */
}

/* ❌  */
.card { padding: 20px; }
.card { padding: 30px !important; }  /*  */

/* ❌  */
.my-component .title {
  font-size: 24px !important;  /*  */
}
```

### 

```css
/* ： .btn  */

/* ❌  !important */
.my-btn {
  background: red !important;
}

/* ✅  */
button.my-btn {
  background: red;
}

/* ✅  */
.container .my-btn {
  background: red;
}

/* ✅  :where()  */
:where(.btn) {
  background: blue;  /*  0 */
}
.my-btn {
  background: red;   /*  */
}
```

### 

```markdown
🔴 [blocking] " 15  !important，"
🟡 [important] " !important "
💡 [suggestion] " CSS Layers (@layer) "
```

---

## 

### 🔴 

#### 1. `transition: all` 

```css
/* ❌  -  */
.button {
  transition: all 0.3s ease;
}

/* ✅  */
.button {
  transition: background-color 0.3s ease, transform 0.3s ease;
}

/* ✅  */
.button {
  --transition-duration: 0.3s;
  transition:
    background-color var(--transition-duration) ease,
    box-shadow var(--transition-duration) ease,
    transform var(--transition-duration) ease;
}
```

#### 2. box-shadow 

```css
/* ❌  -  */
.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s ease;
}
.card:hover {
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}

/* ✅  + opacity */
.card {
  position: relative;
}
.card::after {
  content: '';
  position: absolute;
  inset: 0;
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
  border-radius: inherit;
}
.card:hover::after {
  opacity: 1;
}
```

#### 3. （Reflow）

```css
/* ❌  */
.bad-animation {
  transition: width 0.3s, height 0.3s, top 0.3s, left 0.3s, margin 0.3s;
}

/* ✅  transform  opacity（） */
.good-animation {
  transition: transform 0.3s, opacity 0.3s;
}

/*  translate  top/left */
.move {
  transform: translateX(100px);  /* ✅ */
  /* left: 100px; */             /* ❌ */
}

/*  scale  width/height */
.grow {
  transform: scale(1.1);  /* ✅ */
  /* width: 110%; */      /* ❌ */
}
```

### 🟡 

#### 

```css
/* ❌  -  */
.page .container .content .article .section .paragraph span {
  color: red;
}

/* ✅  */
.article-text {
  color: red;
}

/* ❌  */
* { box-sizing: border-box; }           /*  */
[class*="icon-"] { display: inline; }   /*  */

/* ✅  */
.icon-box * { box-sizing: border-box; }
```

#### 

```css
/* ⚠️  */
.heavy-shadow {
  box-shadow:
    0 1px 2px rgba(0,0,0,0.1),
    0 2px 4px rgba(0,0,0,0.1),
    0 4px 8px rgba(0,0,0,0.1),
    0 8px 16px rgba(0,0,0,0.1),
    0 16px 32px rgba(0,0,0,0.1);  /* 5  */
}

/* ⚠️  GPU */
.blur-heavy {
  filter: blur(20px) brightness(1.2) contrast(1.1);
  backdrop-filter: blur(10px);  /*  */
}
```

### 

```css
/*  will-change （） */
.animated-element {
  will-change: transform, opacity;
}

/*  will-change */
.animated-element.idle {
  will-change: auto;
}

/*  contain  */
.card {
  contain: layout paint;  /*  */
}
```

### 

- [ ]  `transition: all`？
- [ ]  width/height/top/left？
- [ ] box-shadow ？
- [ ]  3 ？
- [ ]  `will-change`？

---

## 

### Mobile First 

```css
/* ✅ Mobile First -  */
.container {
  padding: 16px;
  display: flex;
  flex-direction: column;
}

/*  */
@media (min-width: 768px) {
  .container {
    padding: 24px;
    flex-direction: row;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* ❌ Desktop First -  */
.container {
  max-width: 1200px;
  padding: 32px;
  flex-direction: row;
}

@media (max-width: 1023px) {
  .container {
    padding: 24px;
  }
}

@media (max-width: 767px) {
  .container {
    padding: 16px;
    flex-direction: column;
    max-width: none;
  }
}
```

### 

```css
/* （） */
:root {
  --breakpoint-sm: 640px;   /*  */
  --breakpoint-md: 768px;   /*  */
  --breakpoint-lg: 1024px;  /* / */
  --breakpoint-xl: 1280px;  /*  */
  --breakpoint-2xl: 1536px; /*  */
}

/*  */
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
```

### 

- [ ]  Mobile First？
- [ ] ？
- [ ] ？
- [ ] （rem/em）？
- [ ] （≥44px）？
- [ ] ？

### 

```css
/* ❌  */
.container {
  width: 1200px;
}

/* ✅  +  */
.container {
  width: 100%;
  max-width: 1200px;
  padding-inline: 16px;
}

/* ❌  */
.text-box {
  height: 100px;  /*  */
}

/* ✅  */
.text-box {
  min-height: 100px;
}

/* ❌  */
.small-button {
  padding: 4px 8px;  /* ， */
}

/* ✅  */
.touch-button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}
```

---

## 

### 

|  |  |  |
|------|--------|------|
| CSS Grid |  ✅ | IE  Autoprefixer +  |
| Flexbox |  ✅ |  |
| CSS Variables |  ✅ | IE ， |
| `gap` (flexbox) |  ⚠️ | Safari 14.1+ |
| `:has()` |  ⚠️ | Firefox 121+ |
| `container queries` |  ⚠️ | 2023  |
| `@layer` |  ⚠️ |  |

### 

```css
/* CSS  */
.button {
  background: #3b82f6;              /*  */
  background: var(--color-primary); /*  */
}

/* Flexbox gap  */
.flex-container {
  display: flex;
  gap: 16px;
}
/*  */
.flex-container > * + * {
  margin-left: 16px;
}

/* Grid  */
.grid {
  display: flex;
  flex-wrap: wrap;
}
@supports (display: grid) {
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}
```

### Autoprefixer 

```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('autoprefixer')({
      //  browserslist 
      grid: 'autoplace',  //  Grid （IE ）
      flexbox: 'no-2009', //  flexbox 
    }),
  ],
};

// package.json
{
  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not dead",
    "not ie 11"  // 
  ]
}
```

### 

- [ ]  [Can I Use](https://caniuse.com)？
- [ ] ？
- [ ]  Autoprefixer？
- [ ] browserslist ？
- [ ] ？

---

## Less / Sass 

### 

```scss
/* ❌  -  */
.page {
  .container {
    .content {
      .article {
        .title {
          color: red;  //  .page .container .content .article .title
        }
      }
    }
  }
}

/* ✅  3  */
.article {
  &__title {
    color: red;
  }

  &__content {
    p { margin-bottom: 1em; }
  }
}
```

### Mixin vs Extend vs 

```scss
/*  -  */
$primary-color: #3b82f6;

/* Mixin -  */
@mixin button-variant($bg, $text) {
  background: $bg;
  color: $text;
  &:hover {
    background: darken($bg, 10%);
  }
}

/* Extend - （） */
%visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
}

.sr-only {
  @extend %visually-hidden;
}

/* ⚠️ @extend  */
// 
//  @media 
//  mixin
```

### 

- [ ]  3 ？
- [ ]  @extend？
- [ ] Mixin ？
- [ ]  CSS ？

---

## 

### 🔴 

```markdown
□ transition: all
□  width/height/top/left/margin
□  !important
□ / >3 
□  >4 
```

### 🟡 

```markdown
□ 
□  Desktop First
□  box-shadow 
□ 
□ CSS 
```

### 🟢 

```markdown
□  CSS Grid 
□  CSS 
□  @layer 
□  contain 
```

---

## 

|  |  |
|------|------|
| [Stylelint](https://stylelint.io/) | CSS  |
| [PurgeCSS](https://purgecss.com/) |  CSS |
| [Autoprefixer](https://autoprefixer.github.io/) |  |
| [CSS Stats](https://cssstats.com/) |  CSS  |
| [Can I Use](https://caniuse.com/) |  |

---

## 

- [CSS Performance Optimization - MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/CSS)
- [What a CSS Code Review Might Look Like - CSS-Tricks](https://css-tricks.com/what-a-css-code-review-might-look-like/)
- [How to Animate Box-Shadow - Tobias Ahlin](https://tobiasahlin.com/blog/how-to-animate-box-shadow/)
- [Media Query Fundamentals - MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Media_queries)
- [Autoprefixer - GitHub](https://github.com/postcss/autoprefixer)
