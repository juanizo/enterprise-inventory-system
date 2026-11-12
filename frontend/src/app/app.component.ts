import { Component } from '@angular/core';
import { RouterOutlet, ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { HeaderComponent } from './layout/header/header.component';
import { FooterComponent } from './layout/footer/footer.component';
import { filter } from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HeaderComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = 'rodyman';

  navbar: 'onLight' | 'onDark' = 'onDark';

  constructor(router: Router, activatedRoute: ActivatedRoute) {
    router.events.pipe(filter((event) => event instanceof NavigationEnd)).subscribe(() => {
      let route = activatedRoute;

      while (route.firstChild) {
        route = route.firstChild;
      }

      this.navbar = route.snapshot.data['navbar'] ?? 'onDark';
    });
  }
}
