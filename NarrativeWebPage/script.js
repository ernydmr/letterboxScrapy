function generateText() {
    const container = document.getElementById('text-container');
    const phrases = ["EXPLORE.", "THE.", "NARRATIVE.", "WORLD."]; // Array of phrases
    const verticalSpacing = 40; // Spacing between texts
    const initialTop = 0; // Initial top position for the first text element
    const additionalSpacing = 50; // Additional spacing between phrases

    let top = initialTop;

    // Function to generate a random color
    const getRandomColor = () => {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    };

    // Loop through phrases and create text elements
    phrases.forEach((phrase, index) => {
        const words = phrase.split("  "); // Split phrase into words
        let phraseTop = top; // Store the top position for the current phrase

        // Loop through words and create text elements
        words.forEach(word => {
            const text = document.createElement('div');
            text.textContent = word;
            text.classList.add('dynamic-text');

            // Set horizontal alignment based on index
            const alignment = index % 2 === 0 ? 'left' : 'right';
            text.style[alignment] = '50%'; // Align text to center horizontally

            // Position text vertically with a fixed spacing
            text.style.top = `${phraseTop}px`;

            // Set random color to text
            text.style.color = getRandomColor();

            container.appendChild(text);

            // Increase top for the next word
            phraseTop += verticalSpacing;
        });

        // Increase top for the next phrase
        top = phraseTop + additionalSpacing;
    });
}

// Call the function to generate text
generateText();
