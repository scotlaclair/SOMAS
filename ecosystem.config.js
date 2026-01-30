/**
 * ecosystem.config.js
 * PM2 configuration for [PROJECT_NAME]
 */

module.exports = {
  apps: [
    {
      name: 'service-1',
      script: './services/service-1/dist/index.js',
      cwd: './services/service-1',
      instances: 1,
      env: {
        NODE_ENV: 'development',
        PORT: 3001,
      },
      error_file: '../../logs/services/service-1-error.log',
      out_file: '../../logs/services/service-1-out.log',
      autorestart: true,
      max_memory_restart: '500M',
    },
  ],
};
