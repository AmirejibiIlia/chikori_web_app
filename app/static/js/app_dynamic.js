// Global variables
let products = [];
let paymentMethods = {};
let priceRanges = [];

// Load all dynamic data on page load
window.addEventListener('DOMContentLoaded', async () => {
  console.log('DOM Content Loaded - Starting to load data...');
  try {
    // Load products
    console.log('Loading products...');
    const productsResponse = await fetch('/api/products');
    products = await productsResponse.json();
    console.log('Products loaded:', products.length, 'products');
    
    // Load payment methods
    console.log('Loading payment methods...');
    const paymentMethodsResponse = await fetch('/api/payment-methods');
    const paymentMethodsData = await paymentMethodsResponse.json();
    if (paymentMethodsData.success) {
      paymentMethods = paymentMethodsData.payment_methods;
      console.log('Payment methods loaded:', Object.keys(paymentMethods).length, 'methods');
    }
    
    // Load price ranges
    console.log('Loading price ranges...');
    const priceRangesResponse = await fetch('/api/price-ranges');
    const priceRangesData = await priceRangesResponse.json();
    if (priceRangesData.success) {
      priceRanges = priceRangesData.price_ranges;
      populatePriceFilter();
      console.log('Price ranges loaded:', priceRanges.length, 'ranges');
    }
    
    // Render products
    console.log('Rendering products...');
    renderProducts(products);
    
    // Set up event listeners after DOM is loaded
    const searchInput = document.querySelector('.search-bar input');
    if (searchInput) {
      searchInput.addEventListener('input', handleSearch);
    }
    
    const priceFilter = document.querySelector('.filter-select');
    if (priceFilter) {
      priceFilter.addEventListener('change', handleFilter);
    }
    
    const sortSelect = document.querySelector('.sort-select');
    if (sortSelect) {
      sortSelect.addEventListener('change', handleSort);
    }
  } catch (error) {
    console.error('Failed to load dynamic data:', error);
  }
});

// Populate price filter dropdown dynamically
function populatePriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) return;
  
  // Clear existing options except the first one
  priceFilter.innerHTML = '<option value="">ფასი</option>';
  
  // Add dynamic price ranges
  priceRanges.forEach(range => {
    if (range.value) { // Skip the "All Prices" option as it's already there
      const option = document.createElement('option');
      option.value = range.value;
      option.textContent = range.label;
      priceFilter.appendChild(option);
    }
  });
}

// Search functionality
function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    const filteredProducts = products.filter(product => 
        product.name.toLowerCase().includes(searchTerm)
    );
    renderProducts(filteredProducts);
}

// Filter by price
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
    const searchInput = document.querySelector('.search-bar input');
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    if (searchTerm) {
        filteredProducts = filteredProducts.filter(product =>
            product.name.toLowerCase().includes(searchTerm)
        );
    }

    renderProducts(filteredProducts);
}

// Sort functionality
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
    const priceFilter = document.querySelector('.filter-select');
    const priceRange = priceFilter ? priceFilter.value : '';
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
    const searchInput = document.querySelector('.search-bar input');
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    if (searchTerm) {
        sortedProducts = sortedProducts.filter(product =>
            product.name.toLowerCase().includes(searchTerm)
        );
    }

    renderProducts(sortedProducts);
}

// Render products with dynamic payment options
function renderProducts(productsToRender) {
    console.log('renderProducts called with:', productsToRender.length, 'products');
    const productGrid = document.querySelector('.product-grid');
    console.log('Product grid element:', productGrid);
    
    if (!productGrid) {
        console.error('Product grid element not found!');
        return;
    }
    
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
                    ${generateMainOptions(product.id)}
                </div>
                ${generateSubOptions(product.id)}
            </div>
        </div>
    `).join('');
}

// Generate main payment option buttons dynamically
function generateMainOptions(productId) {
    if (!paymentMethods || Object.keys(paymentMethods).length === 0) {
        return `
            <button class="main-option-btn" onclick="showSubOptions('${productId}', 'later')">განაწილებით</button>
            <button class="main-option-btn" onclick="showSubOptions('${productId}', 'installment')">განვადება</button>
            <button class="main-option-btn" onclick="showSubOptions('${productId}', 'card')">ბარათით გადახდა</button>
        `;
    }
    
    return Object.entries(paymentMethods).map(([methodType, methodData]) => `
        <button class="main-option-btn" onclick="showSubOptions('${productId}', '${methodType}')">${methodData.name}</button>
    `).join('');
}

// Generate sub-options for each payment method dynamically
function generateSubOptions(productId) {
    if (!paymentMethods || Object.keys(paymentMethods).length === 0) {
        return `
            <div class="sub-options" id="${productId}-later" style="display: none;">
                <div class="sub-option" onclick="selectOption('${productId}', 'bog_later', event)">ნაწილ-ნაწილ <img src="https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/bog.png" class="bank-icon" alt="BOG"></div>
                <div class="sub-option" onclick="selectOption('${productId}', 'tbc_later', event)">განაწილება <img src="https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/tbc.png" class="bank-icon" alt="TBC"></div>
            </div>
            <div class="sub-options" id="${productId}-installment" style="display: none;">
                <div class="sub-option" onclick="selectOption('${productId}', 'bog_installment', event)">საქართველოს ბანკი <img src="https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/bog.png" class="bank-icon" alt="BOG"></div>
                <div class="sub-option" onclick="selectOption('${productId}', 'tbc_installment', event)">თიბისი <img src="https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/tbc.png" class="bank-icon" alt="TBC"></div>
            </div>
            <div class="sub-options" id="${productId}-card" style="display: none;">
                <div class="sub-option" onclick="selectOption('${productId}', 'tbc_card', event)">TBC card <img src="https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/tbc.png" class="bank-icon" alt="TBC"></div>
                <div class="sub-option" onclick="selectOption('${productId}', 'bog_card', event)">BoG card <img src="https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/bog.png" class="bank-icon" alt="BOG"></div>
            </div>
        `;
    }
    
    return Object.entries(paymentMethods).map(([methodType, methodData]) => `
        <div class="sub-options" id="${productId}-${methodType}" style="display: none;">
            ${Object.entries(methodData.options).map(([optionKey, optionData]) => `
                <div class="sub-option" onclick="selectOption('${productId}', '${optionKey}', event)">
                    ${optionData.name} <img src="${optionData.icon}" class="bank-icon" alt="${optionData.bank}">
                </div>
            `).join('')}
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

// Move payment logic to a new function
async function processPayment(product, methodType, optionKey, optionData, event) {
    let button = event ? event.target : null;
    let originalText = button ? button.textContent : '';
    try {
        if (button) {
            button.textContent = 'იტვირთება...';
            button.style.pointerEvents = 'none';
        }
        // Prepare request data for dynamic payment
        const requestData = {
            method_type: methodType,
            option_key: optionKey,
            product_id: product.id,
            amount: product.price
        };
        // Log full request details
        console.log(`=== DYNAMIC PAYMENT REQUEST (${optionData.name}) ===`);
        console.log('Request URL:', '/api/dynamic-payment');
        console.log('Request Method:', 'POST');
        console.log('Request Headers:', {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        });
        console.log('Request Body:', JSON.stringify(requestData, null, 2));
        console.log('Product Details:', product);
        console.log('Payment Method:', methodType);
        console.log('Payment Option:', optionKey);
        console.log('Service:', optionData.service);
        // Create dynamic payment request
        const response = await fetch('/api/dynamic-payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        // Log response details
        console.log(`=== DYNAMIC PAYMENT RESPONSE (${optionData.name}) ===`);
        console.log('Response Status:', response.status);
        console.log('Response Status Text:', response.statusText);
        const result = await response.json();
        console.log('Response Body:', JSON.stringify(result, null, 2));
        if (result.success) {
            // Handle different response types
            let redirectUrl = null;
            if (result.payment_url) {
                redirectUrl = result.payment_url;
            } else if (result.application_url) {
                redirectUrl = result.application_url;
            } else if (result.approval_url) {
                redirectUrl = result.approval_url;
            } else if (result.checkout_url) {
                redirectUrl = result.checkout_url;
            } else if (result.redirect_url) {
                redirectUrl = result.redirect_url;
            }
            if (redirectUrl) {
                console.log('Redirecting to:', redirectUrl);
                window.location.href = redirectUrl;
            } else {
                console.log('Payment successful but no redirect URL provided');
                // No alert - silent success
            }
        } else {
            console.error('Payment failed:', result.error || 'Unknown error');
            // No alert - silent failure
        }
    } catch (error) {
        console.error('Payment request failed:', error);
        // No alert - silent failure
    } finally {
        if (button) {
            button.textContent = originalText;
            button.style.pointerEvents = 'auto';
        }
    }
}

// Update showPhoneModal to ask for name and phone
function showPhoneModal(orderInfo, afterSuccess) {
    // Remove any existing modal
    const existing = document.getElementById('phone-modal-overlay');
    if (existing) existing.remove();
    // Create modal HTML
    const modal = document.createElement('div');
    modal.id = 'phone-modal-overlay';
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal-content">
        <button class="modal-close" onclick="document.getElementById('phone-modal-overlay').remove()">&times;</button>
        <h2>ჩაწერეთ თქვენი ნომერი და სახელი</h2>
        <p>ჩვენი ოპერატორი დაგიკავშირდებათ.</p>
        <input type="text" id="user-name-input" placeholder="სახელი და გვარი" style="width: 90%; padding: 0.5rem; margin-bottom: 1rem; font-size: 1rem; border-radius: 6px; border: 1px solid #ccc;" maxlength="50" />
        <input type="text" id="user-phone-input" placeholder="მაგ: 555123456" style="width: 90%; padding: 0.5rem; margin-bottom: 1rem; font-size: 1rem; border-radius: 6px; border: 1px solid #ccc;" maxlength="15" />
        <div class="modal-actions">
          <button class="modal-btn" id="send-order-btn">გაგზავნა</button>
        </div>
        <div id="phone-modal-error" style="color: red; margin-top: 1rem; display: none;"></div>
      </div>
    `;
    document.body.appendChild(modal);
    // Add send button logic
    document.getElementById('send-order-btn').onclick = async function() {
        const name = document.getElementById('user-name-input').value.trim();
        const phone = document.getElementById('user-phone-input').value.trim();
        const errorDiv = document.getElementById('phone-modal-error');
        // Validate name
        if (!name) {
            errorDiv.textContent = 'გთხოვთ, შეიყვანეთ თქვენი სახელი და გვარი';
            errorDiv.style.display = 'block';
            return;
        }
        // Basic phone validation (Georgian mobile: 9 digits, starts with 5)
        if (!/^5\d{8}$/.test(phone)) {
            errorDiv.textContent = 'გთხოვთ, შეიყვანეთ სწორი ნომერი (მაგ: 555123456)';
            errorDiv.style.display = 'block';
            return;
        }
        errorDiv.style.display = 'none';
        // Prepare order info
        const payload = {
            ...orderInfo,
            name: name,
            phone: phone,
            order_time: new Date().toLocaleString('ka-GE', { timeZone: 'Asia/Tbilisi' })
        };
        // Send to backend
        try {
            const resp = await fetch('/api/send-order-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await resp.json();
            if (result.success) {
                document.getElementById('phone-modal-overlay').remove();
                if (typeof afterSuccess === 'function') afterSuccess();
                return;
            } else {
                errorDiv.textContent = result.error || 'შეცდომა გაგზავნისას';
                errorDiv.style.display = 'block';
            }
        } catch (e) {
            errorDiv.textContent = 'შეცდომა გაგზავნისას';
            errorDiv.style.display = 'block';
        }
    };
}

// Patch selectOption to show modal, then process payment after email
async function selectOption(productId, optionKey, event) {
    // Find the product
    const product = products.find(p => p.id === productId);
    if (!product) {
        alert('პროდუქტი ვერ მოიძებნა');
        return;
    }
    // Find the payment method and option
    let methodType = null;
    let optionData = null;
    for (const [type, method] of Object.entries(paymentMethods)) {
        if (method.options && method.options[optionKey]) {
            methodType = type;
            optionData = method.options[optionKey];
            break;
        }
    }
    if (!methodType || !optionData) {
        console.error(`Payment option ${optionKey} not found in configuration`);
        alert('გადახდის მეთოდი ვერ მოიძებნა');
        return;
    }
    // Show phone modal, then process payment after success
    showPhoneModal({
        product_id: product.id,
        product_name: product.name,
        product_price: product.price,
        payment_method: methodType,
        payment_option: optionKey,
        payment_option_name: optionData.name
    }, function() {
        processPayment(product, methodType, optionKey, optionData, event);
    });
}

// Toggle dropdown functionality
function toggleDropdown(productId) {
    const dropdown = document.getElementById(`dropdown-${productId}`);
    if (dropdown) {
        dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
    }
}

// Show sub-options functionality
function showSubOptions(productId, optionType) {
    // Hide all sub-options for this product
    const allSubOptions = document.querySelectorAll(`#${productId}-later, #${productId}-installment, #${productId}-card`);
    allSubOptions.forEach(sub => sub.style.display = "none");
    
    // Remove active class from all buttons in this product's dropdown
    const dropdown = document.getElementById(`dropdown-${productId}`);
    const allButtons = dropdown.querySelectorAll('.main-option-btn');
    allButtons.forEach(btn => btn.classList.remove('active'));
    
    // Add active class to the clicked button
    const clickedButton = event.target;
    clickedButton.classList.add('active');
    
    // Show the selected sub-option
    const targetSubOption = document.getElementById(`${productId}-${optionType}`);
    targetSubOption.style.display = "block";
    
    // Prevent event bubbling
    event.stopPropagation();
} 