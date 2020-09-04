import pygame
import math
import time

class Site:
    def __init__(self,number,x, y, width, height,  color,cont_color):
        self.width = width
        self.height = height
        self.color = color
        self.cont_color = cont_color
        self.number = number
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)

    def get_site_number(self):
        return self.number
    
    def change_color(self, color, cont_color):
        self.color = color
        self.cont_color = cont_color

    def render(self,surface):
        pygame.draw.rect(surface,self.color, self.rect)
        pygame.draw.rect(surface,self.cont_color,self.rect,2)
    def redraw_site(self, surface, color, cont_color):
        self.change_color(color, cont_color)
        self.render(surface)


class SiteGrid:
    def __init__(self, n, start_point, site_size, color, cont_color):
        self.site_grid = []

        x, y = start_point
      
        for i in range(n * n):
            x += site_size
            if not i % n:
                y += site_size
                x = start_point[0]
           
            site = Site(i, x, y, site_size, site_size, color, cont_color)
            self.site_grid.append(site)
    



    def display(self, surface):
        for site in self.site_grid:
            site.render(surface)
 

class Message:
    def __init__(self, surface, msg, font, font_size, msg_center, color, background_color = None):
        
        self.surface = surface
        text_font = pygame.font.Font(font, font_size)
        self.textSurface = text_font.render(msg, True, color, background_color)
        self.textRect = self.textSurface.get_rect(center = msg_center)

    def display_msg(self):
        
        self.surface.blit(self.textSurface, self.textRect)
  
        
    def clear_msg(self):
        clean_surf = self.textRect.inflate(20,0)
        clean_surf = self.surface.subsurface(clean_surf)
        
        if self.background_color:
            clean_surf.fill(self.bacground_color)
        else:
            clean_surf.fill((255,255,255))
        



class Button:
    
    def __init__(self,  x, y, w, h, inactive_color, active_color, text = None, action = None):


        self.text = text
        self.rect = pygame.Rect(x,y,w,h)
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.action = action
        self.hover = False
         

    def text_button(self):
       
        font = pygame.font.Font(None, self.rect[3]//2)
        text_but = font.render(self.text, True, (0,0,0))
        text_but_rect = text_but.get_rect(center = self.rect.center)

        return text_but, text_but_rect

    def get_text(self):
        return self.text
         

    def button_check(self, event):        

        if event.type == pygame.MOUSEMOTION:
               
            self.hover = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.hover and self.action:      
                self.action()


    def button_draw(self, surface, pushed_color = None):
       

        

        if self.hover:
            color = self.active_color
        
        else:
            color = self.inactive_color

        if pushed_color:
            color = pushed_color

        pygame.draw.rect(surface, color, self.rect)
        if self.text:
            text, text_rect = self.text_button()
            surface.blit(text, text_rect)

     
 


class Scale_button:
    
    
    def __init__(self, surface, site,  active_color, push_color, index = None):

        self.surface = surface
        self.site = site
        self.button = Button(site.x, site.y, site.width, site.height,
                             site.color, active_color, str(site.number))  
        self.active_color = active_color
        self.push_color = push_color
        self.index = index
        self.info_msg = None
        self.pushed = False
        


        
 
    def check_scale_button(self, event):
        self.button.button_check(event)
        if event.type == pygame.MOUSEBUTTONUP:
          
            if self.button.hover:
                self.pushed = not self.pushed


    def toggle_buttons(self, button):
        button.pushed, self.pushed = self.pushed, button.pushed
    
            

    def draw_scale_button(self):
       if self.pushed:
           self.button.button_draw(self.surface, self.push_color)
       else:
           self.button.button_draw(self.surface)
       pygame.draw.rect(self.surface, self.site.cont_color, self.button.rect, 2)
       
   
   

    def push_button(self):
        self.info_msg = Message(self.surface, 'You picked ' + str(self.site.number), 'freesansbold.ttf',
                           25, (400,self.site.y + self.site.height + 10), (0, 0, 0), background_color = None)
        self.info_msg.clear_msg()
        self.info_msg.display_msg()
        
        
    def release_button(self):
        
        if self.info_msg:
            self.info_msg.clear_msg()
           
        
       


class Scale:
    THRESHOLD = 500
    
    def __init__(self, surface, x, y, length, height, default_value, start_value, end_value,
                 step, color, cont_color, active_color, push_color):
        
        self.surface = surface
        self.partition_number = (end_value - start_value) // step + 1
        self.step = step
        
        self.partition_size = length // self.partition_number
        self.default_value = default_value

        self.start_value = start_value
        self.x = x
        self.y = y
        self.height = height
        self.color = color
        self.cont_color = cont_color
        self.active_color = active_color
        self.push_color = push_color
        self.scale = []
        self.already_pushed = Scale.THRESHOLD
        
    def set_scale(self):
        number = self.start_value
        x = self.x
        y = self.y
        for i in range(self.partition_number):
            
            partition = Site(number, x, y, self.partition_size, self.height, self.color, self.cont_color)
            s_button = Scale_button(self.surface, partition, self.active_color, self.push_color, i )
           
            self.scale.append(s_button)
            x += self.partition_size
            number += self.step
            


    def get_choice(self):
        if self.already_pushed != Scale.THRESHOLD:
            return self.scale[self.already_pushed].site.number
        return self.default_value

    
        

    def check_scale(self,event):
        i = 0
        while True:
            if i == len(self.scale):
                break
            self.scale[i].check_scale_button(event)
            
            if self.scale[i].pushed and i != self.already_pushed:
                if self.already_pushed != Scale.THRESHOLD:
                    self.scale[self.already_pushed].pushed = False
                self.already_pushed = i
            if not self.scale[i].pushed and self.already_pushed == i:
                self.already_pushed = Scale.THRESHOLD
            
            i += 1
            

    def display_scale(self):
        
        
        for i in range(len(self.scale)):
            
            self.scale[i].draw_scale_button()

