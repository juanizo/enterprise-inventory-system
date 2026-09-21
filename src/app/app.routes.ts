import { Routes } from '@angular/router';
import { MainPageComponent } from './features/main-page/main-page.component';
import { ServiciosComponent } from './features/servicios/servicios.component';
import { NosotrosComponent } from './features/nosotros/nosotros.component';
import { ContactanosComponent } from './features/contactanos/contactanos.component';

export const routes: Routes = [
  {
    path: 'inicio',
    component: MainPageComponent,
    data: { navbar: 'onDark' },
  },
  {
    path: 'servicios',
    component: ServiciosComponent,
    data: { navbar: 'onLight' },
  },
  {
    path: 'nosotros',
    component: NosotrosComponent,
  },
  {
    path: 'contactanos',
    component: ContactanosComponent,
  },
];
