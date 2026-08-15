/**
 * Ranking for shopping-list cards.
 *
 * The dashboard shows only the first few lists, so *which* lists those are
 * matters more than their order within the group. A list you are part-way
 * through is the one you are most likely to open next; a list you have not
 * started is still actionable; a finished or empty list is not.
 *
 * Sorting client-side on purpose: the counts this needs (totalitems,
 * totalpurchased) already come back on ShoppingListOut, so no schema change and
 * no new ordering on GET /shoppinglists — which the API still returns grouped
 * by store, the order the management pages want.
 */

const IN_PROGRESS = 0;
const UNTOUCHED = 1;
const FINISHED = 2;
const EMPTY = 3;

export const rankOf = list => {
  const total = list?.totalitems ?? 0;
  const purchased = list?.totalpurchased ?? 0;

  if (total === 0) return EMPTY;
  if (purchased >= total) return FINISHED;
  if (purchased > 0) return IN_PROGRESS;
  return UNTOUCHED;
};

/**
 * A new array ordered in-progress → untouched → finished → empty.
 *
 * Array.prototype.sort is stable, so lists sharing a rank keep the order the
 * API sent them in (store, then name) rather than shuffling between renders.
 */
export const rankShoppingLists = lists =>
  Array.isArray(lists) ? [...lists].sort((a, b) => rankOf(a) - rankOf(b)) : [];
