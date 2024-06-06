module.exports = {
  preset: 'ts-jest',
  transform: {
    '^.+\\.(t|j)sx?$': '@swc/jest',
  },
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '\\.(css|less|sass|scss)$': '<rootDir>/node_modules/jest-css-modules',
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@utilities/(.*)$': '<rootDir>/src/utilities/$1',
    '^types/(.*)$': '<rootDir>/src/types/$1',
  },
};
