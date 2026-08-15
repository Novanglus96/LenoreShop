/**
 * A repeating set of small angles, so a grid of sheets looks dropped on the
 * page rather than laid out on a grid.
 *
 * Deterministic by index: a random tilt would make cards jump on every
 * re-render, which the realtime sync causes often.
 */
const TILTS = ["-0.7deg", "0.5deg", "-0.3deg", "0.8deg", "-0.5deg"];

export const tiltFor = index => TILTS[index % TILTS.length];
