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

  // 6. Contact Form Submission Handling (Telegram Integration)
  const interestForm = document.getElementById('interest-form');
  
  if (interestForm) {
    interestForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const nameInput = document.getElementById('user-name');
      const phoneInput = document.getElementById('user-phone');
      const prefTypeSelect = document.getElementById('pref-type');
      const residenceInput = document.getElementById('user-residence');
      const visitDateInput = document.getElementById('visit-date');
      const messageInput = document.getElementById('user-message');
      const privacyAgreeCheckbox = document.getElementById('privacy-agree');
      const submitBtn = interestForm.querySelector('.btn-submit');
      
      // Clean up phone number input (digits only)
      const phoneValue = phoneInput.value.replace(/[^0-9]/g, '');
      
      // Validation Check
      if (!nameInput.value.trim()) {
        showToast('이름을 입력해 주세요.', 'error');
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
      
      // Disable submit button and show loading state
      const originalBtnText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.textContent = '등록 중...';
      
      // Format phone number for readability: e.g. 01012345678 -> 010-1234-5678
      let formattedPhone = phoneValue;
      if (phoneValue.length === 11) {
        formattedPhone = `${phoneValue.slice(0, 3)}-${phoneValue.slice(3, 7)}-${phoneValue.slice(7)}`;
      } else if (phoneValue.length === 10) {
        formattedPhone = `${phoneValue.slice(0, 3)}-${phoneValue.slice(3, 6)}-${phoneValue.slice(6)}`;
      }
      
      const prefTypeText = prefTypeSelect.options[prefTypeSelect.selectedIndex].text;
      
      // Get marketing funnel selection
      const funnelCheckboxes = interestForm.querySelectorAll('input[name="funnel"]:checked');
      const funnelValues = Array.from(funnelCheckboxes).map(cb => cb.value).join(', ') || '없음';
      
      // Telegram Bot Details
      const botToken = '8945070290:AAGVX0fHTNAC68BgBBP7DstL2V0PXxEa-wQ';
      const chatId = '8753795118';
      
      const messageText = `✨ [남성역 헤르니티 관심고객 등록] ✨
--------------------------------
👤 이름: ${nameInput.value.trim()}
📞 연락처: ${formattedPhone}
🏠 관심 평형: ${prefTypeText}
📍 현재 거주지: ${residenceInput.value.trim() || '미입력'}
📅 방문희망일시: ${visitDateInput.value.trim() || '미입력'}
💬 문의사항: ${messageInput.value.trim() || '없음'}
🔍 인입 경로: ${funnelValues}
--------------------------------
📅 신청일시: ${new Date().toLocaleString('ko-KR')}`;
      
      fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          chat_id: chatId,
          text: messageText
        })
      })
      .then(response => {
        if (response.ok) {
          // Save data locally as backup
          const registrationData = {
            name: nameInput.value.trim(),
            phone: phoneValue,
            prefType: prefTypeSelect.value,
            residence: residenceInput.value.trim(),
            visitDate: visitDateInput.value.trim(),
            message: messageInput.value.trim(),
            funnel: Array.from(funnelCheckboxes).map(cb => cb.value),
            registeredAt: new Date().toISOString()
          };
          
          let existingList = [];
          try {
            existingList = JSON.parse(localStorage.getItem('hernity_registrations') || '[]');
          } catch (err) {
            existingList = [];
          }
          existingList.push(registrationData);
          localStorage.setItem('hernity_registrations', JSON.stringify(existingList));
          
          // Success Alert
          showToast('상담 신청이 정상적으로 완료되었습니다! 담당자가 곧 연락드리겠습니다.', 'success');
          interestForm.reset();
        } else {
          showToast('등록 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.', 'error');
        }
      })
      .catch(error => {
        console.error('Error sending message:', error);
        showToast('네트워크 오류가 발생했습니다. 인터넷 연결을 확인해 주세요.', 'error');
      })
      .finally(() => {
        // Restore button state
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      });
    });
  }
});
