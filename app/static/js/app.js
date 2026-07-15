document.addEventListener("DOMContentLoaded", function () {
  // Initialize Bootstrap tooltips
  var tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  // Auto-dismiss flash alerts after 5 seconds
  var alerts = document.querySelectorAll(".alert-dismissible");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      var btn = alert.querySelector(".btn-close");
      if (btn) btn.click();
    }, 5000);
  });

  // Sidebar toggle for mobile
  var toggle = document.getElementById("sidebarToggle");
  var sidebar = document.getElementById("sidebar");
  if (toggle && sidebar) {
    toggle.addEventListener("click", function () {
      sidebar.classList.toggle("show");
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener("click", function (e) {
      if (
        window.innerWidth < 992 &&
        sidebar.classList.contains("show") &&
        !sidebar.contains(e.target) &&
        e.target !== toggle
      ) {
        sidebar.classList.remove("show");
      }
    });
  }

  // File upload drag and drop visual feedback
  var dropZone = document.getElementById("dropZone");
  if (dropZone) {
    var fileInput = dropZone.querySelector('input[type="file"]');

    dropZone.addEventListener("dragover", function (e) {
      e.preventDefault();
      dropZone.classList.add("drag-over");
    });

    dropZone.addEventListener("dragleave", function () {
      dropZone.classList.remove("drag-over");
    });

    dropZone.addEventListener("drop", function (e) {
      e.preventDefault();
      dropZone.classList.remove("drag-over");
      if (e.dataTransfer.files.length > 0 && fileInput) {
        fileInput.files = e.dataTransfer.files;
        updateFileLabel(fileInput);
      }
    });

    if (fileInput) {
      fileInput.addEventListener("change", function () {
        updateFileLabel(fileInput);
      });
    }
  }

  function updateFileLabel(input) {
    var label = document.getElementById("fileLabel");
    if (label && input.files.length > 0) {
      var file = input.files[0];
      var size = (file.size / 1024).toFixed(1);
      label.textContent = file.name + " (" + size + " KB)";
      label.classList.remove("text-muted");
      label.classList.add("text-white");
    }
  }

  // Confirm delete with custom styling
  var deleteForms = document.querySelectorAll("form[data-confirm]");
  deleteForms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!confirm(form.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });
});
