class TBCInstallment {
    constructor(apiKey, merchantId) {
        this.apiKey = apiKey;
        this.merchantId = merchantId;
        this.baseUrl = 'https://api.tbcbank.ge/v1/online-installments';
        
        // Campaign IDs for different products - you'll get these from TBC
        this.campaigns = {
            installment_standard: "default_standard", // Regular installment
            installment_split: "default_split"      // Split payment
        };
    }

    async initiateInstallment(productData) {
        try {
            // Select appropriate campaign based on installment type
            const campaignId = this.campaigns[productData.installmentType] || "default_standard";
            
            // Calculate installment details based on type
            const monthlyPayment = this.calculateMonthlyPayment(productData);
            
            const response = await fetch(`${this.baseUrl}/initiate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'apikey': this.apiKey,
                    'merchant-id': this.merchantId
                },
                body: JSON.stringify({
                    priceTotal: productData.price,
                    productId: productData.id,
                    quantity: 1,
                    campaignId: campaignId,
                    pricePerMonth: monthlyPayment,
                    invoiceId: Date.now().toString(),
                    callbackUrl: `${window.location.origin}/tbc-callback`,
                    preAuth: true,
                    installmentType: productData.installmentType
                })
            });

            const data = await response.json();
            if (data.status === 'success') {
                window.location.href = data.redirectUrl;
            } else {
                throw new Error('Failed to initiate installment');
            }
        } catch (error) {
            console.error('TBC Installment Error:', error);
            alert('განვადების ინიციალიზაცია ვერ მოხერხდა. გთხოვთ სცადოთ თავიდან.');
        }
    }

    calculateMonthlyPayment(productData) {
        // Different calculation logic based on installment type
        if (productData.installmentType === 'installment_split') {
            // Split payment - typically divided into 2-4 payments
            return productData.price / 3; // Default to 3 payments for split
        } else {
            // Standard installment - typically 12 months
            return productData.price / 12;
        }
    }
}

// Initialize TBC integration
const tbcInstallment = new TBCInstallment(
    'YOUR_API_KEY_HERE', // Replace with your actual API key
    'YOUR_MERCHANT_ID_HERE' // Replace with your actual merchant ID
); 