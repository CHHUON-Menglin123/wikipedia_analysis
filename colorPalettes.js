const colorPalettes = {
    // Modern and professional palette
    default: [
        '#2c3e50', // Dark blue
        '#e74c3c', // Red
        '#3498db', // Blue
        '#2ecc71', // Green
        '#f1c40f', // Yellow
        '#9b59b6', // Purple
        '#1abc9c', // Turquoise
        '#e67e22', // Orange
        '#34495e', // Navy blue
        '#16a085'  // Dark turquoise
    ],

    // Pastel palette
    pastel: [
        '#FFB3BA', // Pink
        '#BAFFC9', // Mint
        '#BAE1FF', // Light blue
        '#FFFFBA', // Light yellow
        '#FFB3F7', // Light purple
        '#B3FFF9', // Light turquoise
        '#FFC8B3', // Light orange
        '#B3FFB3', // Light green
        '#E0B3FF', // Lavender
        '#FFE4B3'  // Light peach
    ],

    // Dark theme palette
    dark: [
        '#FF6B6B', // Bright red
        '#4ECDC4', // Turquoise
        '#45B7D1', // Light blue
        '#96CEB4', // Sage
        '#FFEEAD', // Light yellow
        '#D4A5A5', // Dusty rose
        '#9A7AA0', // Purple
        '#87A8A4', // Gray-green
        '#F7D794', // Light orange
        '#9AECDB'  // Mint
    ],

    // Nature-inspired palette
    nature: [
        '#88B04B', // Greenery
        '#92A8D1', // Serenity
        '#955251', // Marsala
        '#B565A7', // Radiant orchid
        '#009B77', // Emerald
        '#DD4124', // Tangerine
        '#D94F70', // Honeysuckle
        '#45B5AA', // Turquoise
        '#5B5EA6', // Ultra violet
        '#98B2D1'  // Air force blue
    ],

    // Get colors for specific word frequencies
    getColorForFrequency: function(frequency, maxFrequency, palette = 'default') {
        // Ensure the palette exists, otherwise use default
        const colors = this[palette] || this.default;
        
        // Calculate the color index based on frequency
        const ratio = frequency / maxFrequency;
        const index = Math.floor(ratio * (colors.length - 1));
        
        return colors[index];
    },

    // Get gradient colors for a range
    getGradientColors: function(palette = 'default') {
        const colors = this[palette] || this.default;
        return {
            colors: colors,
            cssGradient: `linear-gradient(45deg, ${colors.join(', ')})`
        };
    }
};

// Function to get a color scheme based on time of day
function getTimeBasedPalette() {
    const hour = new Date().getHours();
    
    if (hour >= 6 && hour < 12) {
        return colorPalettes.nature;     // Morning
    } else if (hour >= 12 && hour < 17) {
        return colorPalettes.default;    // Afternoon
    } else if (hour >= 17 && hour < 20) {
        return colorPalettes.pastel;     // Evening
    } else {
        return colorPalettes.dark;       // Night
    }
}
