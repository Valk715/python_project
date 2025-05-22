document.addEventListener('DOMContentLoaded', function() {

    let inputText = document.getElementById('input-text');
    let outputText = document.getElementById('output-text');
    let encryptBtn = document.getElementById('encrypt-btn')

    let upperCase = ['A','B','C','D','E','F','G','H','I','J','K',
    'L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];

    let lowerCase = ['a','b','c','d','e','f','g','h','i','j','k',
    'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];
    
    function rot13(text) {
        var result = [];
        
        for (let i = 0; i < text.length; i++) {
            let char = text[i];
            let found = false;
            
            // чек на заглавные буквы
            for (let j = 0; j < upperCase.length; j++) {
                if (char === upperCase[j]) {
                    result.push(upperCase[(j + 13) % 26]);
                    found = true;
                    break;
                }
            }
            
            // чек на строчные буквы
            if (!found) {
                for (let j = 0; j < lowerCase.length; j++) {
                    if (char === lowerCase[j]) {
                        result.push(lowerCase[(j + 13) % 26]);
                        found = true;
                        break;
                    }
                }
            }
            
            // Если не буква оставляем 
            if (!found) result.push(char);
        }
        
        let output = '';
        for (let i = 0; i < result.length; i++) {
            output += result[i];
        }
        
        return output;
    }
    
    encryptBtn.addEventListener('click', function() {
        outputText.value = rot13(inputText.value);
    });
});

