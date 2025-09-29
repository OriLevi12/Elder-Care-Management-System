/**
 * Utility functions for formatting data in the caregiver dashboard
 */

export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
};

export const getInitials = (name) => {
  return name.split(' ').map(word => word[0]).join('').toUpperCase();
};
