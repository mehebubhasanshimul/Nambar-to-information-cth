export default async function handler(req, res) {
    const { number } = req.query;

    if (!number) {
        return res.status(400).json({ error: "Number is required" });
    }

    // নম্বর থেকে যদি শুরুতে ০ থাকে তবে তা বাদ দিয়ে ৮৮০ যোগ করা (সেফটি চেক)
    let cleanNumber = number.startsWith('0') ? number.substring(1) : number;
    if (!cleanNumber.startsWith('880')) {
        cleanNumber = '880' + cleanNumber;
    }

    const options = {
        method: 'GET',
        headers: {
            'x-rapidapi-key': process.env.RAPIDAPI_KEY, // Vercel Variables থেকে আসবে
            'x-rapidapi-host': 'truecaller-data2.p.rapidapi.com'
        }
    };

    try {
        const url = `https://truecaller-data2.p.rapidapi.com/search/${cleanNumber}`;
        const response = await fetch(url, options);
        const data = await response.json();
        
        res.status(200).json(data);
    } catch (error) {
        res.status(500).json({ error: "Internal Server Error" });
    }
}
