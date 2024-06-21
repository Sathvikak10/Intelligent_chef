import openai
import os

class RecipeGenerator:
    def __init__(self, openai_api_key, output_folder="generated_recipes"):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def generate_recipe(self, ingredient_list):
        """ Generate a cooking recipe based on the list of ingredients provided. """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI capable of creating delicious and practical recipes. Use the ingredients provided to create a recipe that incorporates all or most of the ingredients effectively."},
                    {"role": "user", "content": ingredient_list}
                ]
            )
            recipe_output = response.choices[0].message.content
            self.save_recipe(recipe_output)
            return recipe_output
        except Exception as e:
            print(f"Error in generating recipe: {e}")
            return []

    def save_recipe(self, recipe_output):
        """ Save the generated recipe to a file. """
        filename = "generated_recipe.txt"
        path = os.path.join(self.output_folder, filename)
        with open(path, 'w') as file:
            file.write(recipe_output)
        print(f"Recipe successfully saved to {path}.")

# Example Usage
if __name__ == "__main__":
    api_key = "insert an apikey"
    generator = RecipeGenerator(api_key)
    ingredient_list = "Apple, Banana, Carrot"  # This would be the output from your object detection
    recipe_output = generator.generate_recipe(ingredient_list)
    print(recipe_output)
