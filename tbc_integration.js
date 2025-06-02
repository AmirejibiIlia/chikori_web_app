class TBCInstallment {
    constructor(apiKey, merchantId) {
        this.apiKey = apiKey;
        this.merchantId = merchantId;
        this.baseUrl = '/api/tbc';
    }

    async initiateInstallment(productData) {
        try {
            console.log('Initiating TBC payment:', productData); // Debug log
            const response = await fetch(`${this.baseUrl}/initiate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(productData)
            });

            const data = await response.json();
            console.log('TBC response:', data); // Debug log
            
            if (data.status === 'success' && data.redirectUrl) {
                window.location.href = data.redirectUrl;
            } else {
                throw new Error(data.message || 'Failed to initiate installment');
            }
        } catch (error) {
            console.error('TBC Installment Error:', error);
            alert('განვადების ინიციალიზაცია ვერ მოხერხდა. გთხოვთ სცადოთ თავიდან.');
        }
    }
}