// import { loadStripe } from '@stripe/stripe-js';

// const STRIPE_PUBLIC_KEY = import.meta.env.VITE_STRIPE_PUBLIC_KEY || 'pk_test_your_key_here';

// export async function createCheckoutSession(teamId: string, plan: string) {
//   try {
//     const response = await fetch('http://localhost:8000/api/payments/create-checkout/', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//         'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
//       },
//       body: JSON.stringify({
//         team_id: teamId,
//         plan: plan,
//       }),
//     });

//     if (!response.ok) {
//       throw new Error('Failed to create checkout session');
//     }

//     const { sessionId } = await response.json();
    
//     const stripe = await loadStripe(STRIPE_PUBLIC_KEY);
    
//     if (!stripe) {
//       throw new Error('Stripe failed to load');
//     }

//     const { error } = await stripe.redirectToCheckout({ sessionId });
    
//     if (error) {
//       throw error;
//     }
//   } catch (error) {
//     console.error('Stripe error:', error);
//     throw error;
//   }
// }

// export async function verifyPayment(sessionId: string) {
//   try {
//     const response = await fetch(`http://localhost:8000/api/payments/verify/${sessionId}/`, {
//       headers: {
//         'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
//       },
//     });

//     if (!response.ok) {
//       throw new Error('Payment verification failed');
//     }

//     return await response.json();
//   } catch (error) {
//     console.error('Verification error:', error);
//     throw error;
//   }
// }