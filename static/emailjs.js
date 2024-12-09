// EMAILJS
document.addEventListener('DOMContentLoaded', function () {
  // Initialize EmailJS with your public key
  emailjs.init('LgALbUXWHpDPxIIRP');

  const contactForm = document.getElementById('contact-form');
  const contactMessage = document.getElementById('contact-message');

  // Log form data as key-value pairs
  const formData = new FormData(contactForm);
  formData.forEach((value, key) => {
      console.log(`${key}: ${value}`);
  });

  const sendEmail = (e) => {
      e.preventDefault(); // prevents the default page reload behavior

      // Log form data again before sending the email
      const formData = new FormData(contactForm);
      formData.forEach((value, key) => {
          console.log(`${key}: ${value}`);
      });

      emailjs.sendForm('service_lqj55s5', 'template_5xzoch8', contactForm)
      .then(() => {
          contactMessage.textContent = 'Message sent successfully ✅';
          setTimeout(() => {
              contactMessage.textContent = '';
          }, 1500);
          contactForm.reset();
      }, (error) => {
          console.error('EmailJS error:', error);
          contactMessage.textContent = 'Message not sent (service error) ❌';
      });
  };

  contactForm.addEventListener('submit', sendEmail);
});
