document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
            this.saveForm()
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            // step 3 validate data
            let categoriesArray = Array.from(document.getElementsByClassName('js-categories-input'));
            let institutionsCategoryArray = Array.from(document.getElementsByClassName('js-organisation-categories'))

            const buttons = document.getElementsByClassName('js-categories-btn');

            // download checked category with category.id in data-set


            // compare checked category with institutions

            buttons[1].addEventListener('click', function () {
                categoriesArray.forEach(function ( category){
                    if (category.checked) {
                        institutionsCategoryArray.forEach(function (element){
                            if (!element.dataset.id.includes (category.dataset.id)) {
                                element.remove()
                        }})}})})




            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;


            // TODO: get data from inputs and show them in summary

            buttons[3].addEventListener('click', function (){

                const bags_amount = document.getElementById('bags').value;
                const bags_summary = document.querySelector('[data-bags="data-bags"]')

                let chosenCategory = document.querySelector('input[name="categories"]:checked')
                console.log(chosenCategory)
                console.log(chosenCategory)
                bags_summary.innerText= bags_amount + " worki " + chosenCategory.value

                const institution_summary = document.querySelector('[data-organisation="data-organisation"]')
                let institution_chosen = document.querySelector('input[name="institution"]:checked')
                institution_summary.innerText = institution_chosen.value

                const date_table = document.getElementById("date_table").children
                const address_table = document.getElementById("address_table").children

                date_table[0].innerHTML = document.getElementById('data').value
                date_table[1].innerHTML = document.getElementById('time').value
                date_table[2].innerHTML = document.getElementById('more_info').value

                console.log(chosenCategory)
                address_table[0].innerHTML = document.getElementById('address').value
                address_table[1].innerHTML = document.getElementById('city').value
                address_table[2].innerHTML = document.getElementById('postcode').value
                address_table[3].innerHTML = document.getElementById('phone').value
                                                           })

            // const form = document.getElementById('form')
            // const submit_button = document.getElementsByClassName('js-submit-btn')
            // submit_button[0].addEventListener('submit', form.submit)
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        saveForm() {
//             function logFormSubmit(event){
//                 console.log('Form submitted! ');
//                 event.preventDefault();
//
// }
//             const my_form = document.getElementById('form')
//             my_form.addEventListener('submit', logFormSubmit)

            const my_form = document.getElementById('form')
            const submit_button = document.getElementsByClassName('js-submit-btn')
            submit_button[0].addEventListener('click', function (){
                my_form.requestSubmit()
                console.log('form submit')
            })
        }



        submit(e) {
            // dodać wyjątek dla konkretnegu buttona tpu submit
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
            // this.saveForm()


        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});
