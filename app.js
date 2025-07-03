// Product data structure
let products = [
    {
        id: 'table',
        name: 'კარადა',
        price: 51,
        rating: 4.9,
        image: 'https://gorgia.ge/images/ab__webp/thumbnails/1223/1000/detailed/53/BM-00146724_-_Closet_jpg.webp',
        sku: 'TABLE_001',
        description: '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> 100x182x52 - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> MDF<br><strong>ფერი:</strong> თეთრი<br><strong>დამზადების ვადა:</strong> 3 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი</strong>'
    },
    {
        id: 'bed',
        name: 'საწოლი',
        price: 51,
        rating: 4.7,
        image: 'https://gorgia.ge/images/ab__webp/thumbnails/1223/1000/detailed/64/BM-00201015-_1__jpg.webp',
        sku: 'BED_001',
        description: '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> Queen Size - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> მეტალი<br><strong>ფერი:</strong> შავი<br><strong>დამზადების ვადა:</strong> 3 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი</strong>'
    },
    {
        id: 'sofa',
        name: 'სამზარეულოს კუთხე',
        price: 51,
        rating: 5.0,
        image: 'https://zeelproject.com/uploads/posts/2021-02-15/1613392761_2.jpg',
        sku: 'SOFA_001',
        description: '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> 124x164x83 - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> MDF/LMNT<br><strong>ფერი:</strong> ხისფერი (მონაცრისფრო)<br><strong>დამზადების ვადა:</strong> 2 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი</strong>'
    },
    {
        id: 'desk',
        name: 'სამუშაო მაგიდა',
        price: 51,
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
                    <div class="sub-option" onclick="selectOption('${product.id}', 'ნაწილ-ნაწილ', event)">ნაწილ-ნაწილ <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/bog.png" class="bank-icon" alt="BOG"></div>
                    <div class="sub-option" onclick="selectOption('${product.id}', 'განაწილება', event)">განაწილება <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/tbc.png" class="bank-icon" alt="TBC"></div>
                </div>
                <div class="sub-options" id="${product.id}-installment" style="display: none;">
                    <div class="sub-option" onclick="selectOption('${product.id}', 'საქართველოს ბანკი', event)">საქართველოს ბანკი <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/bog.png" class="bank-icon" alt="BOG"></div>
                    <div class="sub-option" onclick="selectOption('${product.id}', 'თიბისი', event)">თიბისი <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/tbc.png" class="bank-icon" alt="TBC"></div>
                </div>
                <div class="sub-options" id="${product.id}-card" style="display: none;">
                    <div class="sub-option" onclick="selectOption('${product.id}', 'TBC card', event)">TBC card <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/tbc.png" class="bank-icon" alt="TBC"></div>
                    <div class="sub-option" onclick="selectOption('${product.id}', 'BoG card', event)">BoG card <img src="https://extra.ge/assets/atomic-assets/img/svg-icons/bog.png" class="bank-icon" alt="BOG"></div>
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
async function selectOption(productId, option, event) {
    console.log(`Selected ${option} for ${productId}`);
    
    // Find the product
    const product = products.find(p => p.id === productId);
    if (!product) {
        alert('პროდუქტი ვერ მოიძებნა');
        return;
    }
    
    // Handle TBC card payment
    if (option === 'TBC card') {
        let button = event ? event.target : null;
        let originalText = button ? button.textContent : '';
        try {
            if (button) {
                button.textContent = 'იტვირთება...';
                button.style.pointerEvents = 'none';
            }
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
                if (button) {
                    button.textContent = originalText;
                    button.style.pointerEvents = 'auto';
                }
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
            if (button) {
                button.textContent = originalText;
                button.style.pointerEvents = 'auto';
            }
        }
    } 
    // Handle TBC installment payment
    else if (option === 'თიბისი') {
        let button = event ? event.target : null;
        let originalText = button ? button.textContent : '';
        try {
            if (button) {
                button.textContent = 'იტვირთება...';
                button.style.pointerEvents = 'none';
            }
            // Prepare request data
            const requestData = {
                product_id: productId,
                amount: product.price
            };
            
            // Log full request details
            console.log('=== TBC INSTALLMENT REQUEST ===');
            console.log('Request URL:', '/api/tbc-installment');
            console.log('Request Method:', 'POST');
            console.log('Request Headers:', {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            });
            console.log('Request Body:', JSON.stringify(requestData, null, 2));
            console.log('Product Details:', product);
            
            // Create installment application request
            const response = await fetch('/api/tbc-installment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            // Log response details
            console.log('=== TBC INSTALLMENT RESPONSE ===');
            console.log('Response Status:', response.status);
            console.log('Response Status Text:', response.statusText);
            console.log('Response Headers:', Object.fromEntries(response.headers.entries()));
            
            const result = await response.json();
            console.log('Response Body:', JSON.stringify(result, null, 2));
            
            if (result.success && result.redirect_url) {
                // Store session ID for potential cancel/confirm operations
                if (result.session_id) {
                    localStorage.setItem('tbc_session_id', result.session_id);
                    localStorage.setItem('tbc_invoice_id', result.invoice_id);
                }
                
                // Redirect to TBC installment application page
                window.location.href = result.redirect_url;
            } else {
                // Show error with debug info
                const errorMessage = `❌ TBC Installment request failed!

Error: ${result.error || 'Unknown error'}
Details: ${JSON.stringify(result.debug_info || {}, null, 2)}

Check browser console for full request/response details.`;
                
                alert(errorMessage);
                // Reset button
                if (button) {
                    button.textContent = originalText;
                    button.style.pointerEvents = 'auto';
                }
            }
            
        } catch (error) {
            console.error('=== TBC INSTALLMENT ERROR ===');
            console.error('Error:', error);
            console.error('Error Message:', error.message);
            console.error('Error Stack:', error.stack);
            
            const errorMessage = `❌ TBC Installment request failed!

Network Error: ${error.message}
Check browser console for full error details.`;
            
            alert(errorMessage);
            // Reset button
            if (button) {
                button.textContent = originalText;
                button.style.pointerEvents = 'auto';
            }
        }
    }
    // Handle TBC E-Commerce installment payment (განაწილება)
    else if (option === 'განაწილება') {
        let button = event ? event.target : null;
        let originalText = button ? button.textContent : '';
        try {
            if (button) {
                button.textContent = 'იტვირთება...';
                button.style.pointerEvents = 'none';
            }
            // Prepare request data
            const requestData = {
                product_id: productId,
                amount: product.price
            };
            
            // Log full request details
            console.log('=== TBC E-COMMERCE PAYMENT REQUEST ===');
            console.log('Request URL:', '/api/tbc-ecommerce-payment');
            console.log('Request Method:', 'POST');
            console.log('Request Headers:', {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            });
            console.log('Request Body:', JSON.stringify(requestData, null, 2));
            console.log('Product Details:', product);
            
            // Create E-Commerce payment request
            const response = await fetch('/api/tbc-ecommerce-payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            // Log response details
            console.log('=== TBC E-COMMERCE PAYMENT RESPONSE ===');
            console.log('Response Status:', response.status);
            console.log('Response Status Text:', response.statusText);
            console.log('Response Headers:', Object.fromEntries(response.headers.entries()));
            
            const result = await response.json();
            console.log('Response Body:', JSON.stringify(result, null, 2));
            
            if (result.success && result.approval_url) {
                // Store payment ID for potential operations
                if (result.pay_id) {
                    localStorage.setItem('tbc_ecommerce_pay_id', result.pay_id);
                    localStorage.setItem('tbc_ecommerce_merchant_payment_id', result.merchant_payment_id);
                }
                
                // Redirect to TBC E-Commerce payment page
                window.location.href = result.approval_url;
            } else {
                // Show user-friendly error message
                let errorMessage = '❌ TBC E-Commerce payment request failed!\n\n';
                
                if (result.error && result.error.includes('access token')) {
                    errorMessage += 'TBC E-Commerce credentials are not configured or invalid.\n\n';
                    errorMessage += 'This feature requires proper TBC E-Commerce API credentials.\n';
                    errorMessage += 'Please contact support for assistance.';
                } else {
                    errorMessage += `Error: ${result.error || 'Unknown error'}\n\n`;
                    errorMessage += 'Check browser console for full details.';
                }
                
                alert(errorMessage);
                // Reset button
                button.textContent = originalText;
                button.style.pointerEvents = 'auto';
            }
            
        } catch (error) {
            console.error('=== TBC E-COMMERCE PAYMENT ERROR ===');
            console.error('Error:', error);
            console.error('Error Message:', error.message);
            console.error('Error Stack:', error.stack);
            
            const errorMessage = `❌ TBC E-Commerce payment request failed!

Network Error: ${error.message}
Check browser console for full error details.`;
            
            alert(errorMessage);
            // Reset button
            button.textContent = originalText;
            button.style.pointerEvents = 'auto';
        }
    } else {
        // For other payment options, show alert (placeholder)
        alert(`თქვენ აირჩიეთ: ${option}`);
    }
    
    // Prevent event bubbling
    if (event) {
        event.stopPropagation();
    }
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

// Intercept purchase button clicks - no restrictions
function interceptPurchaseButtons() {
  const purchaseButtons = document.querySelectorAll('.buy-now, .purchase-btn');
  purchaseButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
      // Allow normal flow - no restrictions
    });
  });
}

// Run on page load
window.addEventListener('DOMContentLoaded', interceptPurchaseButtons); 