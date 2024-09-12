document.addEventListener('DOMContentLoaded', () => {
    const navItems = document.querySelectorAll('.navItem');
    const mobileNavItems = document.querySelectorAll('.mobileNavItem');
    const activeContainer = document.querySelector('.navItemActiveContainer');
    const mobileActiveContainer = document.querySelector('.mobilenavItemActiveContainer');
    const burgerMenu = document.querySelector('.burgerMenu');
    const mobileNav = document.querySelector('.mobileNav');
  
    let selectedIndexDesktop = -1;
    let selectedIndexMobile = -1;
  
    if (navItems && activeContainer) {
      const positions = [570, 370, 170, -30];
      navItems.forEach((item, index) => {
        item.addEventListener('click', () => {
          activeContainer.style.right = positions[index] + 'px';
          selectedIndexDesktop = index;
          updateNavItemState(navItems, selectedIndexDesktop, 'desktop');
        });
      });
    }
  
    if (mobileNavItems && mobileActiveContainer) {
      const mobilePositions = [210, 140, 70, 0];
      mobileNavItems.forEach((item, index) => {
        item.addEventListener('click', () => {
          mobileActiveContainer.style.bottom = mobilePositions[index] + 'px';
          selectedIndexMobile = index;
          updateNavItemState(mobileNavItems, selectedIndexMobile, 'mobile');
        });
      });
    }
  
    function updateNavItemState(items, index, type) {
      items.forEach((item, i) => {
        if (i === index) {
          item.classList.add(type === 'mobile' ? 'mobileActive' : 'active');
        } else {
          item.classList.remove(type === 'mobile' ? 'mobileActive' : 'active');
        }
      });
    }
  
    if (burgerMenu && mobileNav) {
      burgerMenu.addEventListener('click', () => {
        if (mobileNav.style.display === 'none' || mobileNav.style.display === '') {
          mobileNav.style.display = 'flex';
        } else {
          mobileNav.style.display = 'none';
        }
      });
    }
  })

  document.addEventListener('DOMContentLoaded', () => {
    const navItems = document.querySelectorAll('.navItem2');
    const mobileNavItems = document.querySelectorAll('.mobileNavItem2');
    const activeContainer = document.querySelector('.navItemActiveContainer2');
    const mobileActiveContainer = document.querySelector('.mobilenavItemActiveContainer2');
    const burgerMenu = document.querySelector('.burgerMenu2');
    const mobileNav = document.querySelector('.mobileNav2');
  
    let selectedIndexDesktop = -1;
    let selectedIndexMobile = -1;
  
    if (navItems && activeContainer) {
      const positions = [570, 370, 170, -30];
      navItems.forEach((item, index) => {
        item.addEventListener('click', () => {
          activeContainer.style.right = positions[index] + 'px';
          selectedIndexDesktop = index;
          updateNavItemState(navItems, selectedIndexDesktop, 'desktop');
        });
      });
    }
  
    if (mobileNavItems && mobileActiveContainer) {
      const mobilePositions = [210, 140, 70, 0];
      mobileNavItems.forEach((item, index) => {
        item.addEventListener('click', () => {
          mobileActiveContainer.style.bottom = mobilePositions[index] + 'px';
          selectedIndexMobile = index;
          updateNavItemState(mobileNavItems, selectedIndexMobile, 'mobile');
        });
      });
    }
  
    function updateNavItemState(items, index, type) {
      items.forEach((item, i) => {
        if (i === index) {
          item.classList.add(type === 'mobile' ? 'mobileActive' : 'active');
        } else {
          item.classList.remove(type === 'mobile' ? 'mobileActive' : 'active');
        }
      });
    }
  
    if (burgerMenu && mobileNav) {
      burgerMenu.addEventListener('click', () => {
        if (mobileNav.style.display === 'none' || mobileNav.style.display === '') {
          mobileNav.style.display = 'flex';
        } else {
          mobileNav.style.display = 'none';
        }
      });
    }
  })