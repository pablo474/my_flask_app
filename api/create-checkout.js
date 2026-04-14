const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { amount, zone, object_price, shipping } = req.body;
    const total = parseFloat(amount);

    if (!total || total < 7) {
      return res.status(400).json({ error: 'El precio mínimo es 7€' });
    }

    const line_items = [
      {
        price_data: {
          currency: 'eur',
          product_data: {
            name: 'YONKO — EP Artoy',
            description: 'Figura impresa en 3D · edición limitada · sin pintar · llave secreta BlindBox',
            images: ['https://yonko.art/static/images/caratula_EP_1.PNG'],
          },
          unit_amount: Math.round(parseFloat(object_price) * 100),
        },
        quantity: 1,
      },
      {
        price_data: {
          currency: 'eur',
          product_data: {
            name: 'Envío — ' + (zone || 'Internacional'),
          },
          unit_amount: Math.round(parseFloat(shipping) * 100),
        },
        quantity: 1,
      }
    ];

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items,
      mode: 'payment',
      shipping_address_collection: {
        allowed_countries: ['ES', 'FR', 'DE', 'IT', 'PT', 'GB', 'US', 'MX', 'AR', 'CL', 'CO', 'PE', 'EC', 'UY', 'PY', 'BO', 'VE', 'CR', 'PA', 'DO'],
      },
      success_url: 'https://yonko.art/desktop.html?pago=ok',
      cancel_url: 'https://yonko.art/desktop.html?open=artoys',
    });

    res.status(200).json({ url: session.url });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Error al crear la sesión de pago' });
  }
};
