//const API_URL = "http://localhost:8000/search";

const API_URL = "/search";

async function searchItems() {
    const query = document.getElementById('searchInput').value;
    const resultsContainer = document.getElementById('resultsSection');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');

    // Clear previous results
    resultsContainer.innerHTML = '';
    errorDiv.classList.add('hidden');

    if (!query) {
        alert("Please enter a query.");
        return;
    }

    loadingDiv.classList.remove('hidden');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const items = await response.json();

        loadingDiv.classList.add('hidden');

        if (items.length === 0) {
            errorDiv.textContent = "No items found matching your criteria.";
            errorDiv.classList.remove('hidden');
            return;
        }

        displayItems(items);

    } catch (error) {
        loadingDiv.classList.add('hidden');
        console.error("Error fetching data:", error);

        // Demo fallback if backend is not reachable
        if (error.message.includes("Failed to fetch") || error.message.includes("NetworkError")) {
             displayMockData();
             errorDiv.innerHTML = `<strong>Backend unreachable. Showing mock data for demo purpose.</strong><br/>(${error.message})`;
             errorDiv.classList.remove('hidden');
        } else {
            errorDiv.textContent = `Error: ${error.message}`;
            errorDiv.classList.remove('hidden');
        }
    }
}

function displayItems(items) {
    const resultsContainer = document.getElementById('resultsSection');

    items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'product-card';

        card.innerHTML = `
            <img src="${item.image_url}" alt="${item.name}" class="product-image" onerror="this.src='https://placehold.co/300x300?text=No+Image'">
            <div class="product-details">
                <div class="product-name">${item.name}</div>
                <div class="product-info">Category: ${item.category}</div>
                <div class="product-info">Size: ${item.size}</div>
                <div class="product-info">Color: ${item.color}</div>
                <div class="product-price">$${item.price.toFixed(2)}</div>
            </div>
        `;

        resultsContainer.appendChild(card);
    });
}

function displayMockData() {
    const mockItems = [
        {
            name: "Blue Running Shoes",
            category: "Boys",
            size: "7",
            color: "Blue",
            price: 45.99,
            image_url: "https://placehold.co/300x300?text=Blue+Shoes"
        },
        {
            name: "Blue Sneakers",
            category: "Boys",
            size: "7",
            color: "Blue",
            price: 49.99,
            image_url: "https://placehold.co/300x300?text=Blue+Sneakers"
        }
    ];
    displayItems(mockItems);
}

// Allow Enter key to search
document.getElementById('searchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchItems();
    }
});
