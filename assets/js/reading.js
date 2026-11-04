const narrow = matchMedia('(max-width: 900px)');
for (const contents of document.querySelectorAll('.page-contents')) {
  const fitLayout = () => { contents.open = !narrow.matches; };
  fitLayout();
  narrow.addEventListener('change', fitLayout);
  contents.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link || !narrow.matches) return;
    const target = document.getElementById(link.hash.slice(1));
    if (!target) return;
    // Move keyboard focus before collapsing the currently focused link.
    target.tabIndex = -1;
    target.focus({ preventScroll: true });
    contents.open = false;
  });
}
