# BusTicket - Enhanced Bus Booking Platform

A modern, AI-powered bus booking platform inspired by BookMeBus.com with enhanced features for the AI era. Built with React, TailwindCSS, and Framer Motion.

## 🚀 Features

### Core Features
- **Multi-Service Booking**: Bus, Private Transfer, Airport Transfer, Ferry
- **Smart Search**: Intelligent origin/destination suggestions
- **Route Discovery**: Popular routes with detailed information
- **Responsive Design**: Mobile-first, works on all devices
- **Modern UI/UX**: Beautiful animations and smooth interactions

### AI-Enhanced Features
- **AI-Powered Route Suggestions**: Personalized recommendations
- **Smart Price Prediction**: Market trend analysis for best booking times
- **Real-time Availability**: ML algorithms for accurate seat availability
- **24/7 AI Assistant**: Intelligent chatbot support
- **Smart Notifications**: Proactive travel alerts
- **Multi-language Support**: AI-powered translation

### Technical Features
- **React 19**: Latest React with hooks
- **TailwindCSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations and transitions
- **Lucide React**: Beautiful icons
- **Responsive Design**: Mobile-first approach
- **SEO Optimized**: Semantic HTML structure

## 🛠️ Technology Stack

- **Frontend**: React 19, TailwindCSS, Framer Motion
- **Icons**: Lucide React
- **Styling**: PostCSS, Autoprefixer
- **Build Tool**: Create React App with CRACO
- **Package Manager**: Yarn

## 📦 Installation

### Prerequisites
- Node.js (version 16 or higher)
- Yarn package manager
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd busticket-clone
   ```

2. **Install dependencies**
   ```bash
   cd frontend
   yarn install
   ```

3. **Start development server**
   ```bash
   yarn start
   ```

4. **Open in browser**
   ```
   http://localhost:3000
   ```

## 🌐 Deployment

### Production Build

1. **Build for production**
   ```bash
   cd frontend
   yarn build
   ```

2. **Test production build locally**
   ```bash
   # Install serve globally
   npm install -g serve
   
   # Serve the build folder
   serve -s build -l 3000
   ```

### Deployment Options

#### Option 1: Netlify (Recommended)
1. Build the project: `yarn build`
2. Drag and drop the `build` folder to Netlify
3. Configure custom domain: `busticket.khdot.com`

#### Option 2: Vercel
1. Connect your GitHub repository
2. Set build command: `yarn build`
3. Set output directory: `build`
4. Configure custom domain

#### Option 3: Traditional Web Hosting
1. Build the project: `yarn build`
2. Upload contents of `build` folder to your web server
3. Configure web server to serve `index.html` for all routes

#### Option 4: Docker Deployment
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . .
RUN yarn build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Option 5: AWS S3 + CloudFront
1. Build the project: `yarn build`
2. Upload to S3 bucket
3. Configure CloudFront distribution
4. Set up custom domain

### Server Configuration

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name busticket.khdot.com;
    
    location / {
        root /path/to/build;
        try_files $uri $uri/ /index.html;
    }
    
    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Apache Configuration
```apache
<VirtualHost *:80>
    ServerName busticket.khdot.com
    DocumentRoot /path/to/build
    
    <Directory /path/to/build>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    # Handle React Router
    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.html [L]
</VirtualHost>
```

## 🔧 Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_BACKEND_URL=https://your-backend-url.com
REACT_APP_API_KEY=your-api-key
REACT_APP_GOOGLE_MAPS_API_KEY=your-google-maps-key
```

## 🚀 Performance Optimization

### Build Optimizations
- Code splitting with React.lazy()
- Image optimization with WebP format
- Bundle analysis with webpack-bundle-analyzer
- Tree shaking for unused code elimination

### Runtime Optimizations
- Service worker for caching
- Lazy loading for images and components
- Debounced search inputs
- Virtualization for large lists

## 🔒 Security

- Input sanitization
- XSS protection
- CSRF protection
- Secure headers configuration
- Content Security Policy

## 🧪 Testing

```bash
# Run tests
yarn test

# Run tests with coverage
yarn test --coverage

# Run tests in watch mode
yarn test --watch
```

## 📱 Progressive Web App (PWA)

The application includes PWA features:
- Service worker for offline functionality
- App manifest for installability
- Push notifications support
- Background sync

## 🌍 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📊 Analytics Integration

Add Google Analytics or your preferred analytics:

```javascript
// Add to public/index.html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🔄 Continuous Integration/Deployment

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          yarn install
      - name: Build
        run: |
          cd frontend
          yarn build
      - name: Deploy to Netlify
        uses: netlify/actions/deploy@master
        with:
          publish-dir: './frontend/build'
          production-branch: main
```

## 🛡️ Monitoring

- Error tracking with Sentry
- Performance monitoring
- User analytics
- Server monitoring

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support, email support@busticket.khdot.com or create an issue in the repository.

## 🔮 Future Enhancements

- Backend API integration
- User authentication
- Payment gateway integration
- Seat selection interface
- Booking management system
- Real-time tracking
- Mobile app development

---

Built with ❤️ for the AI era of travel booking.