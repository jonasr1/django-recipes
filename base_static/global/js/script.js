function my_scope() {
  const forms = document.querySelectorAll(".form-delete");
  for (const form of forms) {
    form.addEventListener("submit", function(e) {
      e.preventDefault();
      const confimed = confirm("Are you sure?");
      if (confimed ){
        form.submit();
      }
    });
  }
}
my_scope()