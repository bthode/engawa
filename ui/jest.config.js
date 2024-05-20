module.exports = {
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest',
  },
  testEnvironment: "jest-environment-jsdom",
  moduleNameMapper: {
    '\\.(css|less|sass|scss)$': '<rootDir>/node_modules/jest-css-modules',
  },
};

