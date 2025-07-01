// Product data structure
let products = [
    {
        id: 'table',
        name: 'კარადა',
        price: 250,
        rating: 4.9,
        image: 'https://gorgia.ge/images/ab__webp/thumbnails/1223/1000/detailed/53/BM-00146724_-_Closet_jpg.webp',
        sku: 'TABLE_001',
        description: '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> 100x182x52 - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> MDF<br><strong>ფერი:</strong> თეთრი<br><strong>დამზადების ვადა:</strong> 3 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი</strong>'
    },
    {
        id: 'bed',
        name: 'საწოლი',
        price: 650,
        rating: 4.7,
        image: 'https://gorgia.ge/images/ab__webp/thumbnails/1223/1000/detailed/64/BM-00201015-_1__jpg.webp',
        sku: 'BED_001',
        description: '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> Queen Size - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> მეტალი<br><strong>ფერი:</strong> შავი<br><strong>დამზადების ვადა:</strong> 3 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი</strong>'
    },
    {
        id: 'sofa',
        name: 'სამზარეულოს კუთხე',
        price: 650,
        rating: 5.0,
        image: 'https://zeelproject.com/uploads/posts/2021-02-15/1613392761_2.jpg',
        sku: 'SOFA_001',
        description: '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> 124x164x83 - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> MDF/LMNT<br><strong>ფერი:</strong> ხისფერი (მონაცრისფრო)<br><strong>დამზადების ვადა:</strong> 2 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი</strong>'
    },
    {
        id: 'desk',
        name: 'სამუშაო მაგიდა',
        price: 400,
        rating: 4.8,
        image: 'https://gorgia.ge/images/ab__webp/thumbnails/1223/1000/detailed/65/BM-00141262_jpg.webp',
        sku: 'DESK_001',
        description: '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> 140x70x40 - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> MDF/LMNT<br><strong>ფერი:</strong> ხისფერი<br><strong>დამზადების ვადა:</strong> 3 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი</strong>'
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
            <div class="product-image-wrapper">
                <img class="product-image" src="${product.image}" alt="${product.name}" />
            </div>
            <div class="product-info">
                <div class="wishlist-icon">
                    <i class="far fa-heart"></i>
                </div>
                <h3>${product.name}</h3>
                <div class="product-description">${product.description}</div>
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
                    <button class="main-option-btn" onclick="showSubOptions('${product.id}', 'later')">განაწილებით</button>
                    <button class="main-option-btn" onclick="showSubOptions('${product.id}', 'installment')">განვადება</button>
                    <button class="main-option-btn" onclick="showSubOptions('${product.id}', 'card')">ბარათით გადახდა</button>
                </div>
                <div class="sub-options" id="${product.id}-later" style="display: none;">
                    <div class="sub-option" onclick="selectOption('${product.id}', 'ნაწილ-ნაწილ')">ნაწილ-ნაწილ <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/bog.png" class="bank-icon" alt="BOG"></div>
                    <div class="sub-option" onclick="selectOption('${product.id}', 'განაწილება')">განაწილება <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/tbc.png" class="bank-icon" alt="TBC"></div>
                </div>
                <div class="sub-options" id="${product.id}-installment" style="display: none;">
                    <div class="sub-option" onclick="selectOption('${product.id}', 'საქართველოს ბანკი')">საქართველოს ბანკი <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/bog.png" class="bank-icon" alt="BOG"></div>
                    <div class="sub-option" onclick="selectOption('${product.id}', 'თიბისი')">თიბისი <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/tbc.png" class="bank-icon" alt="TBC"></div>
                </div>
                <div class="sub-options" id="${product.id}-card" style="display: none;">
                    <div class="sub-option" onclick="selectOption('${product.id}', 'TBC card')">TBC card <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/tbc.png" class="bank-icon" alt="TBC"></div>
                    <div class="sub-option" onclick="selectOption('${product.id}', 'BoG card')">BoG card <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/bog.png" class="bank-icon" alt="BOG"></div>
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

// Payment processing function
async function selectOption(productId, option) {
    console.log(`Selected ${option} for ${productId}`);
    
    // Find the product
    const product = products.find(p => p.id === productId);
    if (!product) {
        alert('პროდუქტი ვერ მოიძებნა');
        return;
    }
    
    // Handle TBC card payment
    if (option === 'TBC card') {
        try {
            // Show loading state
            const button = event.target;
            const originalText = button.textContent;
            button.textContent = 'იტვირთება...';
            button.style.pointerEvents = 'none';
            
            // Prepare request data
            const requestData = {
                product_id: productId,
                amount: product.price
            };
            
            // Log full request details
            console.log('=== TBC CARD PAYMENT REQUEST ===');
            console.log('Request URL:', '/api/create-payment');
            console.log('Request Method:', 'POST');
            console.log('Request Headers:', {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            });
            console.log('Request Body:', JSON.stringify(requestData, null, 2));
            console.log('Product Details:', product);
            
            // Create payment request
            const response = await fetch('/api/create-payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            // Log response details
            console.log('=== TBC CARD PAYMENT RESPONSE ===');
            console.log('Response Status:', response.status);
            console.log('Response Status Text:', response.statusText);
            console.log('Response Headers:', Object.fromEntries(response.headers.entries()));
            
            const result = await response.json();
            console.log('Response Body:', JSON.stringify(result, null, 2));
            
            // Show debug info in browser console and optionally in an alert
            if (result.success && result.checkout_url) {
                // Redirect directly to Flitt payment page without showing success message
                window.location.href = result.checkout_url;
            } else {
                // Show error with debug info
                const errorMessage = `❌ Payment request failed!

Error: ${result.error || 'Unknown error'}
Details: ${JSON.stringify(result.details || {}, null, 2)}

Check browser console for full request/response details.`;
                
                alert(errorMessage);
                // Reset button
                button.textContent = originalText;
                button.style.pointerEvents = 'auto';
            }
            
        } catch (error) {
            console.error('=== TBC CARD PAYMENT ERROR ===');
            console.error('Error:', error);
            console.error('Error Message:', error.message);
            console.error('Error Stack:', error.stack);
            
            const errorMessage = `❌ Payment request failed!

Network Error: ${error.message}
Check browser console for full error details.`;
            
            alert(errorMessage);
            // Reset button
            const button = event.target;
            button.textContent = originalText;
            button.style.pointerEvents = 'auto';
        }
    } else {
        // For other payment options, show alert (placeholder)
        alert(`თქვენ აირჩიეთ: ${option}`);
    }
    
    // Prevent event bubbling
    event.stopPropagation();
}

// On page load, check for ?search= in URL and filter products
window.addEventListener('DOMContentLoaded', function() {
    const params = new URLSearchParams(window.location.search);
    const searchParam = params.get('search');
    if (searchParam) {
        if (searchInput) searchInput.value = searchParam;
        const filteredProducts = products.filter(product => 
            product.name.toLowerCase().includes(searchParam.toLowerCase())
        );
        renderProducts(filteredProducts);
    } else {
        renderProducts(products);
    }
});

// Render products on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() {
    renderProducts(products);
  });
} else {
  renderProducts(products);
}

// Intercept purchase button clicks
function interceptPurchaseButtons() {
  const purchaseButtons = document.querySelectorAll('.buy-now, .purchase-btn');
  purchaseButtons.forEach(btn => {
    btn.addEventListener('click', async function(e) {
      // Check login status
      const res = await fetch('/api/user-status');
      const data = await res.json();
      if (!data.logged_in) {
        e.preventDefault();
        showLoginModal();
        return false;
      }
      // else: allow normal flow
    });
  });
}

// Run on page load
window.addEventListener('DOMContentLoaded', interceptPurchaseButtons); 