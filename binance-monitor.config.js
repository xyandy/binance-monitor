module.exports = {
  apps: [
    {
      name: 'binance-monitor',
      script: 'main.py',
      interpreter: 'python',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      env: {
        NODE_ENV: 'development',
      },
    },
  ],
};
