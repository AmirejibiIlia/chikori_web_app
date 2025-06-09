// Product data structure
let products = [
    {
        id: 'table',
        name: 'კარადა',
        price: 250,
        rating: 4.0,
        image: 'https://gorgia.ge/images/ab__webp/thumbnails/1223/1000/detailed/53/BM-00146724_-_Closet_jpg.webp',
        sku: 'TABLE_001'
    },
    {
        id: 'bed',
        name: 'საწოლი',
        price: 650,
        rating: 4.5,
        image: 'https://gorgia.ge/images/ab__webp/thumbnails/1223/1000/detailed/64/BM-00201015-_1__jpg.webp',
        sku: 'BED_001'
    },
    {
        id: 'sofa',
        name: 'სამზარეულოს კუთხე',
        price: 650,
        rating: 5.0,
        image: 'https://gorgia.ge/images/ab__webp/thumbnails/1100/900/detailed/5/ab071780-2-_1__jpg.webp',
        sku: 'SOFA_001'
    },
    {
        id: 'desk',
        name: 'სამუშაო მაგიდა',
        price: 400,
        rating: 4.0,
        image: 'https://gorgia.ge/images/ab__webp/thumbnails/1223/1000/detailed/65/BM-00141262_jpg.webp',
        sku: 'DESK_001'
    }
];

// Search functionality
const searchInput = document.querySelector('.search-bar input');
searchInput.addEventListener('input', handleSearch);

function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    const filteredProducts = products.filter(product => 
        product.name.toLowerCase().includes(searchTerm)
    );
    renderProducts(filteredProducts);
}

// Filter by price
const priceFilter = document.querySelector('.filter-select');
priceFilter.addEventListener('change', handleFilter);

function handleFilter(e) {
    const priceRange = e.target.value;
    let filteredProducts = [...products];

    if (priceRange) {
        const [min, max] = priceRange.split('-').map(Number);
        filteredProducts = products.filter(product => {
            if (max) {
                return product.price >= min && product.price <= max;
            } else {
                return product.price >= min;
            }
        });
    }

    // Apply any existing search term
    const searchTerm = searchInput.value.toLowerCase();
    if (searchTerm) {
        filteredProducts = filteredProducts.filter(product =>
            product.name.toLowerCase().includes(searchTerm)
        );
    }

    renderProducts(filteredProducts);
}

// Sorting functionality
const sortSelect = document.querySelector('.sort-select');
sortSelect.addEventListener('change', handleSort);

function handleSort(e) {
    const sortType = e.target.value;
    let sortedProducts = [...products];

    switch (sortType) {
        case 'price-low':
            sortedProducts.sort((a, b) => a.price - b.price);
            break;
        case 'price-high':
            sortedProducts.sort((a, b) => b.price - a.price);
            break;
        case 'newest':
            // In a real application, you would have a date field to sort by
            // For now, we'll just reverse the array as an example
            sortedProducts.reverse();
            break;
    }

    // Apply any existing filters
    const priceRange = priceFilter.value;
    if (priceRange) {
        const [min, max] = priceRange.split('-').map(Number);
        sortedProducts = sortedProducts.filter(product => {
            if (max) {
                return product.price >= min && product.price <= max;
            } else {
                return product.price >= min;
            }
        });
    }

    // Apply any existing search term
    const searchTerm = searchInput.value.toLowerCase();
    if (searchTerm) {
        sortedProducts = sortedProducts.filter(product =>
            product.name.toLowerCase().includes(searchTerm)
        );
    }

    renderProducts(sortedProducts);
}

// Render products
function renderProducts(productsToRender) {
    const productGrid = document.querySelector('.product-grid');
    productGrid.innerHTML = productsToRender.map(product => `
        <div class="product-card" id="${product.id}">
            <div class="product-info">
                <div class="wishlist-icon">
                    <i class="far fa-heart"></i>
                </div>
                <img class="product-image" src="${product.image}" alt="${product.name}" />
                <h3>${product.name}</h3>
                <div class="product-meta">
                    <p class="price">₾${product.price}</p>
                    <div class="rating">
                        ${generateRatingStars(product.rating)}
                        <span>(${product.rating})</span>
                    </div>
                </div>
                <button class="purchase-btn" onclick="toggleDropdown('${product.id}')">შეძენა</button>
            </div>
            <div class="dropdown" id="dropdown-${product.id}" style="display: none;">
                <h3>💳 გადახდის მეთოდები</h3>
                <div class="main-options">
                    <button class="main-option-btn" onclick="showSubOptions('${product.id}', 'later')">გადახდა განაწილებით</button>
                    <button class="main-option-btn" onclick="showSubOptions('${product.id}', 'installment')">განვადება</button>
                </div>
                <div class="sub-options" id="${product.id}-later" style="display: none;">
                    <div class="sub-option" onclick="selectOption('${product.id}', 'ნაწილ-ნაწილ')">ნაწილ-ნაწილ 🟠</div>
                    <div class="sub-option" onclick="initiateTBCInstallment('${product.id}', ${product.price}, '${product.sku}', 'installment_split')">განაწილება 🔵</div>
                </div>
                <div class="sub-options" id="${product.id}-installment" style="display: none;">
                    <div class="sub-option" onclick="selectOption('${product.id}', 'საქართველოს ბანკი')">საქართველოს ბანკი 🟠</div>
                    <div class="sub-option" onclick="initiateTBCInstallment('${product.id}', ${product.price}, '${product.sku}', 'installment_standard')">თიბისი 🔵</div>
                </div>
            </div>
        </div>
    `).join('');
}

// Helper function to generate rating stars
function generateRatingStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= Math.floor(rating)) {
            stars += '<i class="fas fa-star"></i>';
        } else if (i - 0.5 <= rating) {
            stars += '<i class="fas fa-star-half-alt"></i>';
        } else {
            stars += '<i class="far fa-star"></i>';
        }
    }
    return stars;
}

// Initialize wishlist functionality
document.addEventListener('click', function(e) {
    if (e.target.closest('.wishlist-icon')) {
        const icon = e.target.closest('.wishlist-icon').querySelector('i');
        icon.classList.toggle('far');
        icon.classList.toggle('fas');
    }
});

// TBC Integration
function initiateTBCInstallment(productId, price, sku, installmentType) {
    const productCard = document.getElementById(productId);
    const productName = productCard.querySelector('h3').textContent;
    
    const productData = {
        id: sku,
        price: price,
        name: productName,
        installmentType: installmentType
    };
    
    console.log('Product data:', productData); // Debug log
    window.tbcInstallment.initiateInstallment(productData);
    
    // Prevent event bubbling
    event.stopPropagation();
} 