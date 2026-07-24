/* ==========================================
   남성역 헤르니티 - Interactive Scripts
   ========================================== */

document.addEventListener('DOMContentLoaded', () => {
  
  // 1. Sticky Header Scroll Effect
  const header = document.getElementById('header');
  const topBtn = document.getElementById('top-btn');
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    
    // Top button visibility
    if (window.scrollY > 500) {
      topBtn.classList.add('visible');
    } else {
      topBtn.classList.remove('visible');
    }
  });

  // 2. Mobile Hamburger Menu Toggle
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const mobileOverlay = document.getElementById('mobile-overlay');
  const mobileLinks = document.querySelectorAll('.mobile-link');
  
  function toggleMobileMenu() {
    mobileMenuBtn.classList.toggle('active');
    mobileOverlay.classList.toggle('active');
    document.body.classList.toggle('no-scroll');
  }
  
  mobileMenuBtn.addEventListener('click', toggleMobileMenu);
  
  // Close menu when link is clicked
  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (mobileOverlay.classList.contains('active')) {
        toggleMobileMenu();
      }
    });
  });

  // 3. Tab System (Generation & Plan)
  const tabTriggers = document.querySelectorAll('.tab-trigger');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabTriggers.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const targetId = trigger.getAttribute('data-target');
      
      // Remove active states
      tabTriggers.forEach(t => t.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      
      // Add active state to clicked tab & content
      trigger.classList.add('active');
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add('active');
      }
    });
  });

  // 4. Smooth Scrolling for Navigation Links
  const allNavLinks = document.querySelectorAll('a[href^="#"]');
  
  allNavLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        const offset = header.offsetHeight;
        const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY - offset;
        
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // Scroll to Top Button Action
  topBtn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  // 5. Custom Toast Notification System
  const toastContainer = document.getElementById('toast-container');
  
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    
    // Add success icon
    const checkIcon = `<span class="toast-success-icon">✓</span>`;
    toast.innerHTML = `${checkIcon} <span>${message}</span>`;
    
    toastContainer.appendChild(toast);
    
    // Trigger transition reflow
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);
    
    // Fade out and remove toast after 3 seconds
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        toast.remove();
      }, 300);
    }, 3000);
  }

  // 6. Contact Form Submission Handling
  const interestForm = document.getElementById('interest-form');
  
  if (interestForm) {
    interestForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const nameInput = document.getElementById('user-name');
      const phoneInput = document.getElementById('user-phone');
      const prefTypeSelect = document.getElementById('pref-type');
      const privacyAgreeCheckbox = document.getElementById('privacy-agree');
      
      // Clean up phone number input (digits only)
      const phoneValue = phoneInput.value.replace(/[^0-9]/g, '');
      
      // Validation Check
      if (!nameInput.value.trim()) {
        showToast('성함을 입력해 주세요.', 'error');
        nameInput.focus();
        return;
      }
      
      if (!phoneValue || phoneValue.length < 9 || phoneValue.length > 11) {
        showToast('올바른 연락처 번호를 입력해 주세요.', 'error');
        phoneInput.focus();
        return;
      }
      
      if (!prefTypeSelect.value) {
        showToast('관심 평형을 선택해 주세요.', 'error');
        prefTypeSelect.focus();
        return;
      }
      
      if (!privacyAgreeCheckbox.checked) {
        showToast('개인정보 동의 약관에 동의하셔야 등록이 가능합니다.', 'error');
        return;
      }
      
      // Save data locally (Simulated server request)
      const registrationData = {
        name: nameInput.value.trim(),
        phone: phoneValue,
        prefType: prefTypeSelect.value,
        chkResident: document.getElementById('chk-resident').checked,
        chkHouse: document.getElementById('chk-house').checked,
        registeredAt: new Date().toISOString()
      };
      
      // Retrieve existing registrations
      let existingList = [];
      try {
        existingList = JSON.parse(localStorage.getItem('hernity_registrations') || '[]');
      } catch (err) {
        existingList = [];
      }
      
      existingList.push(registrationData);
      localStorage.setItem('hernity_registrations', JSON.stringify(existingList));
      
      // Success Alert
      showToast('관심고객 등록이 정상적으로 완료되었습니다! 분양 안내 정보가 곧 발송됩니다.', 'success');
      
      // Reset form
      interestForm.reset();
    });
  }

});
