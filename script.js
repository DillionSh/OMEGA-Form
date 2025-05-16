translations
language = English
setLanguage(language) {
 this.language = language
//        async function loadTranslations(language) {
//            const response = await fetch('translations.json');
//
//            const translations = await response.json();
//            const langData = translations[language];
//
//            if (langData) {
//
//                document.getElementById('formTitle').textContent = langData.formTitle;
//                document.getElementById('label_name').textContent = langData.label_name;
//                document.getElementById('label_gender').textContent = langData.label_gender;
//                document.getElementById('label_male').textContent = langData.label_male;
//                document.getElementById('label_female').textContent = langData.label_female;
//                document.getElementById('label_unknown').textContent = langData.label_unknown;
//                document.getElementById('label_date_of_birth').textContent = langData.label_date_of_birth;
//                document.getElementById('label_finNum').textContent = langData.label_finNum;
//                document.getElementById('label_sgMobileNum').textContent = langData.label_sgMobileNum;
//                document.getElementById('label_homeCountryMobileNum').textContent = langData.label_homeCountryMobileNum;
//                document.getElementById('label_country').textContent = langData.label_country;
//                document.getElementById('label_yearJoined').textContent = langData.label_yearJoined;
//                document.getElementById('label_languages').textContent = langData.label_languages;
//                document.getElementById('label_Myanmar').textContent = langData.label_Myanmar;
//                document.getElementById('label_India').textContent = langData.label_India;
//                document.getElementById('label_SriLanka').textContent = langData.label_SriLanka;
//                document.getElementById('label_Indonesia').textContent = langData.label_Indonesia;
//                document.getElementById('label_Bangladesh').textContent = langData.label_Bangladesh;
//                document.getElementById('label_Nepal').textContent = langData.label_Nepal;
//                document.getElementById('label_submit').textContent = langData.label_submit;
//                document.getElementById('instructions').textContent = langData.instructions;
//                document.getElementById('instructions_2').textContent = langData.instructions_2;
//                document.getElementById('header').textContent = langData.header;






            } else {
                console.error('Language not found!');
            }
        }

        function setLanguage(language) {
            loadTranslations(language);
        }

        document.addEventListener('DOMContentLoaded', () => {
            loadTranslations('english');
        });


    document.addEventListener('DOMContentLoaded', function () {
    const errorMessage = document.getElementById('alert');

    if (errorMessage) {
        const closeButton = document.createElement('button');
        closeButton.textContent = 'X';
        closeButton.style.float = 'right';
        closeButton.style.background = 'none';
        closeButton.style.border = 'none';
        closeButton.style.color = '#0c0d0c';
        closeButton.style.cursor = 'pointer';
        closeButton.style.fontSize = '16px';
        closeButton.style.marginRight = '10px';

        closeButton.addEventListener('click', function () {
            errorMessage.style.display = 'none';
        });

        errorMessage.appendChild(closeButton);
    }
});
